
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('general/', include('userFolder.urls')),
    path('seeker/', include('seekerFolder.urls')),
    path('jobrecru/', include('recruiter.urls')),
    path('admin/', include('adminpage.urls')),
    path('analytics/', include('analytics.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
