from django.urls import path
from . import views

urlpatterns = [
    path('gr', views.get_recommendations),
    path('gc', views.get_compatibility),

    path('cmp', views.count_my_posts),
    path('cma', views.count_my_applicants),
    path('cmm', views.count_my_messages),

    # Seeker's dashboard
    path('sgs', views.stat_for_seekers),

    # reports in pdf
    path('pdf/user-overview', views.get_useroverview),
    path('pdf/jobpost-insights', views.get_jobpost_insights),
    path('pdf/resume-insights', views.get_resume_insights),
    path('pdf/application-insights', views.get_application_insights),
]
