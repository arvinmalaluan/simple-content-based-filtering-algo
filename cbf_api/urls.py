from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('general/', include('cbf_app.urls')),
]
