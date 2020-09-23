from django.urls import path
from .views import *

urlpatterns = [
    path('portal/', portal, name="portal"),
    path('new_job_application/', new_job_application, name="new_job_application"),
    path(r'job/<int:pk>/', job, name="job"),
    path(r'delete_job/<int:pk>/', delete_job, name="delete_job"),
    path(r'update_job_notes/<int:pk>/', update_job_notes, name="update_job_notes"),
    path('view_all_applications/', view_all_applications, name="view_all_applications"),
]