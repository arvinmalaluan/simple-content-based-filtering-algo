from django.urls import path
from .views import get_recommendations, get_compatibility

urlpatterns = [
    path('gr', get_recommendations),
    path('gc', get_compatibility),
]
