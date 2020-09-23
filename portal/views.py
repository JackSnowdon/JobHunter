from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *

# Create your views here.

@login_required
def portal(request):
    profile = request.user.profile
    jobs = Job.objects.order_by("date")
    return render(request, "portal.html", {"profile": profile, "jobs": jobs})


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