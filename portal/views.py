from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, timedelta
from .models import *
from .forms import *

# Create your views here.

@login_required
def portal(request):
    profile = request.user.profile
    jobs = profile.jobs.all().order_by("date")
    today = date.today()
    today_jobs = jobs.filter(date=today)
    yday = today - timedelta(days=1)
    yday_jobs = jobs.filter(date=yday)
    return render(request, "portal.html", {"profile": profile, "jobs": jobs, "today_jobs": today_jobs, "today": today,
                                            "yday": yday, "yday_jobs": yday_jobs})


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
def update_job_notes(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.profile == request.user.profile:
        if request.method == "POST":
            job_form = JobNotesForm(request.POST, instance=job)
            if job_form.is_valid():
                form = job_form.save(commit=False)
                form.save()
                messages.error(request, f"Update {job} Notes", extra_tags="alert")
                return redirect("job", job.pk)    
        else:
            job_form = JobNotesForm(instance=job)
        return render(request, "update_job_notes.html", {"job_form": job_form, "job": job})
    else:
        messages.error(request, f"Job Not Yours To Update", extra_tags="alert")
        return redirect("index")


@login_required
def view_all_applications(request):
    profile = request.user.profile
    jobs = profile.jobs.all().order_by("date")
    return render(request, "view_all_applications.html", {"jobs": jobs})