from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from datetime import date, timedelta
from .models import *
from .forms import *

# Create your views here.

# Jobs

@login_required
def portal(request):
    profile = request.user.profile
    jobs = profile.jobs.all().order_by("-date").filter(archived=False)
    today, today_jobs = get_single_day_jobs(jobs, 0)
    yday, yday_jobs = get_single_day_jobs(jobs, 1)
    week_ago = today - timedelta(days=7)
    week_jobs = jobs.filter(date__gte=week_ago)
    cons = profile.connects.all()
    _, today_cons_total = get_single_day_cons(cons, 0)
    _, yday_cons_total = get_single_day_cons(cons, 1)
    return render(request, "portal.html", {"profile": profile, "jobs": jobs, "today_jobs": today_jobs, "today": today,
                                            "yday": yday, "yday_jobs": yday_jobs, "week_ago": week_ago, "week_jobs": week_jobs,
                                            "today_cons_total": today_cons_total, "yday_cons_total": yday_cons_total})


def get_single_day_jobs(jobs, day_counter):
    """
    Takes queryset and int for days
    0 for today
    1 for yesterday
    so on
    return (Sorted Data, Date)
    """
    today = date.today()
    if day_counter == 0:
        sorted_jobs = jobs.filter(date=today)
        return today, sorted_jobs
    else:
        day = today - timedelta(days=day_counter)
        sorted_jobs = jobs.filter(date=day)
        return day, sorted_jobs


@login_required
def new_job_application(request):
    if request.method == "POST":
        job_form = NewJobForm(request.POST)
        if job_form.is_valid():
            form = job_form.save(commit=False)
            form.profile = request.user.profile
            form.save()
            messages.error(request, "Created New Application", extra_tags="alert")
            return redirect("portal")    
    else:
        job_form = NewJobForm()
    return render(request, "new_job_application.html", {"job_form": job_form})


@login_required
def job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    profile = request.user.profile
    return render(request, "job.html", {"job": job})


@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.profile == request.user.profile:
        job.delete()
        messages.error(
            request, f"Deleted {job}", extra_tags="alert"
        )
        return redirect(reverse("portal"))
    else:
        messages.error(request, f"Job Not Yours To Delete", extra_tags="alert")
        return redirect("party_home")


@login_required
def update_job_status(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.profile == request.user.profile:
        if request.method == "POST":
            job_form = JobStatusForm(request.POST, instance=job)
            if job_form.is_valid():
                form = job_form.save(commit=False)
                form.save()
                messages.error(request, f"Updated {job} Status", extra_tags="alert")
                return redirect("job", job.pk)    
        else:
            job_form = JobStatusForm(instance=job)
        return render(request, "update_job_status.html", {"job_form": job_form, "job": job})
    else:
        messages.error(request, f"Job Not Yours To Update", extra_tags="alert")
        return redirect("index")


@login_required
def update_job_company(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.profile == request.user.profile:
        if request.method == "POST":
            job_form = JobCompanyForm(request.POST, instance=job)
            if job_form.is_valid():
                form = job_form.save(commit=False)
                form.save()
                messages.error(request, f"Updated {job} Company", extra_tags="alert")
                return redirect("job", job.pk)    
        else:
            job_form = JobCompanyForm(instance=job)
        return render(request, "update_job_company.html", {"job_form": job_form, "job": job})
    else:
        messages.error(request, f"Job Not Yours To Update", extra_tags="alert")
        return redirect("index")


@login_required
def view_all_applications(request):
    profile = request.user.profile
    jobs = profile.jobs.all().order_by("-date").filter(archived=False)
    return render(request, "view_all_applications.html", {"jobs": jobs})


@login_required
def filtered_applications(request, filt):
    profile = request.user.profile
    if filt == "Archived":
        jobs = profile.jobs.all().order_by("-date").filter(archived=True)
    else:
        jobs = profile.jobs.all().order_by("-date").filter(status=filt, archived=False)
    return render(request, "filtered_applications.html", {"jobs": jobs, "filt": filt})


@login_required
def change_job_archive(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.profile == request.user.profile:
        if job.archived == False:
            job.archived = True
            messages.error(request, f"{job} Archived", extra_tags="alert")
        else:
            job.archived = False
            messages.error(request, f"{job} Unarchived", extra_tags="alert")
        job.save()
        return redirect("job", job.pk)
    else:
        messages.error(request, f"Job Not Yours To Update", extra_tags="alert")
        return redirect("index")


# Notes

@login_required
def new_note(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.profile == request.user.profile:
        if request.method == "POST":
            note_form = NewNoteForm(request.POST)
            if note_form.is_valid():
                form = note_form.save(commit=False)
                form.job = job
                form.save()
                messages.error(request, f"Updated {job} Notes", extra_tags="alert")
                return redirect("job", job.pk)  
        else:
            note_form = NewNoteForm()
        return render(request, "new_note.html", {"note_form": note_form, "job": job})
    else:
        messages.error(request, f"Job Not Yours To Update", extra_tags="alert")
        return redirect("index")


@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    job = note.job
    if job.profile == request.user.profile:
        note.delete()
        messages.error(
            request, f"Deleted {note}", extra_tags="alert"
        )
        return redirect("job", job.pk)  
    else:
        messages.error(request, f"Note Not Yours To Delete", extra_tags="alert")
        return redirect("party_home")


# Connections

@login_required
def connections(request):
    profile = request.user.profile
    cons = profile.connects.all().order_by("-date")
    today = date.today()
    if cons.count() == 0:
        messages.error(request, f"Log Connections To Access Connections", extra_tags="alert")
        return redirect("new_connection_entry")
    total_cons = get_sum_value(cons, "all")
    week_cons_total = get_sum_value(cons, 6)
    last_week_dates = return_day_list(today, 6)
    last_week_dates.reverse()
    weeks_data = return_day_values(last_week_dates, cons)
    return render(request, "connections.html", {"cons": cons, "today": today,
                                            "total_cons": total_cons,
                                            "week_cons_total": week_cons_total, "weeks_data": weeks_data})


def return_day_list(today, days):
    """
    Takes today (datetime)
    days(amount of days from today) (datetime)
    
    returns list of days between two dates formated for zingcharts
    """
    start_date = today - timedelta(days=days)
    day_base = today - start_date
    day_list = []
    for i in range(day_base.days + 1):
        day = start_date + timedelta(days=i)
        day_list.append(day)
    return day_list


def return_day_values(day_list, dataset):
    """
    Takes day_list and dataset

    returns fomrated graph data for workout on each day
    """
    value_list = []
    for day in day_list:
        total_amount = 0
        for c in dataset:
            if c.date == day:
                total_amount += c.amount
        value_list.append(total_amount)
    info = dict(zip(day_list, value_list))
    return info
    

def get_sum_value(con_query, counter):
    """
    Takes queryset and int for amount
    0 for today only
    1 for today + yesterday
    2 for tday + yday + day before
    so on
    return total
    """
    today = date.today()
    if counter == 0:
        cons = con_query.filter(date=today)
    elif counter == "all":
        ob = con_query.last()
        start_date = ob.date
        cons = con_query.filter(date__gte=start_date)
    else:
        day = today - timedelta(days=counter)
        cons = con_query.filter(date__gte=day)
    con_dict = cons.aggregate(Sum('amount'))
    con_list = list(con_dict.values())[0]
    return con_list


def get_single_day_cons(cons, counter):
    """
    Takes queryset and int for amount
    0 for today
    1 for yesterday
    so on
    return total
    """
    today = date.today()
    if counter == 0:
        day = today
        target_cons = cons.filter(date=today)
    else:
        day = today - timedelta(days=counter)
        target_cons = cons.filter(date=day)
    con_dict = target_cons.aggregate(Sum('amount'))
    total = list(con_dict.values())[0]
    if total == None:
        total = 0
    return day, total


@login_required
def new_connection_entry(request):
    if request.method == "POST":
        con_form = NewConnectionForm(request.POST)
        if con_form.is_valid():
            form = con_form.save(commit=False)
            form.profile = request.user.profile
            form.save()
            messages.error(request, f"{form.amount} New Connections Added", extra_tags="alert")
            return redirect("connections")  
    else:
        con_form = NewConnectionForm()
    return render(request, "new_connection_entry.html", {"con_form": con_form})


# Calls

@login_required
def call_index(request):
    return render(request, "call_index.html")