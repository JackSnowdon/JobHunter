from django.urls import path
from .views import *

urlpatterns = [
    path('portal/', portal, name="portal"),
]