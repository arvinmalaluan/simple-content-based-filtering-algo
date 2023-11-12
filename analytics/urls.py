from django.urls import path
from . import views

urlpatterns = [
    path('gr', views.get_recommendations),
    path('gc', views.get_compatibility),

    # reports in pdf
    path('pdf/user-overview', views.get_useroverview),
]
