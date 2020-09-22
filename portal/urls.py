from django.urls import path
from .views import *

urlpatterns = [
    path('portal/', portal, name="portal"),
    path('new_job_application/', new_job_application, name="new_job_application"),
    path(r'job/<int:pk>/', job, name="job"),
]