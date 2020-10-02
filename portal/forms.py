from django import forms
from .models import *


class NewJobForm(forms.ModelForm):

    class Meta:
        model = Job
        exclude = ['profile', 'archived']


class JobStatusForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['status']


class JobCompanyForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['company']


class NewNoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['content']


class NewConnectionForm(forms.ModelForm):

    class Meta:
        model = Connection
        fields = ['amount']


class NewCallForm(forms.ModelForm):

    class Meta:
        model = Call
        fields = ['caller', 'notes']

