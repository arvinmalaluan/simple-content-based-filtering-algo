from django.urls import path
from . import views

urlpatterns = [
  path('jobpost', views.provide_compatible_jobs),
  path('compatibiltiy', views.provide_compatibility),
]