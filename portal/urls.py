from django.urls import path
from .views import *

urlpatterns = [
    path('portal/', portal, name="portal"),
    path('new_job_application/', new_job_application, name="new_job_application"),
    path(r'job/<int:pk>/', job, name="job"),
    path(r'delete_job/<int:pk>/', delete_job, name="delete_job"),
    path(r'update_job_notes/<int:pk>/', update_job_notes, name="update_job_notes"),
    path(r'update_job_status/<int:pk>/', update_job_status, name="update_job_status"),
    path(r'update_job_company/<int:pk>/', update_job_company, name="update_job_company"),
    path('view_all_applications/', view_all_applications, name="view_all_applications"),
    path(r'filtered_applications/<str:filt>/', filtered_applications, name="filtered_applications"),
    path(r'new_note/<int:pk>/', new_note, name="new_note"),
]