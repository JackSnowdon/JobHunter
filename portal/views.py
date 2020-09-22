from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import *

# Create your views here.

@login_required
def portal(request):
    profile = request.user.profile
    jobs = Job.objects.order_by("date")
    return render(request, "portal.html", {"profile": profile, "jobs": jobs})
