from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@login_required
def portal(request):
    profile = request.user.profile
    return render(request, "portal.html", {"profile": profile})
