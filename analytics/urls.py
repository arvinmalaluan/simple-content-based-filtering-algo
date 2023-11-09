from django.urls import path
from . import views

urlpatterns = [
    path('gr', views.get_recommendations),
    path('gc', views.get_compatibility),

    # Recruiter's dashboard
    path('cmp', views.count_my_posts),
    path('cma', views.count_my_applicants),
    path('cmm', views.count_my_messages),

    # Seeker's dashboard
    path('sgs', views.stat_for_seekers),
]
