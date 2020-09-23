from django import forms
from .models import *


class NewJobForm(forms.ModelForm):

    class Meta:
        model = Job
        exclude = ['profile']


class JobNotesForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['notes']


class JobStatusForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['status']