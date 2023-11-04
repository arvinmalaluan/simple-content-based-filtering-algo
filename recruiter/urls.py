from django.urls import path

from . import views

urlpatterns = [
    # Get and Post links
    path('jobpost', views.GP_JobPost.as_view()),
    path('post/<int:id>', views.GA_MyJobPosts.as_view()),
    path('all-jobpost', views.GA_JobPost.as_view()),
    path('recru-profile', views.GP_RecruiterProfile.as_view()),
    path('', views.GA_JobPostWApplicants.as_view()),
    path('apply', views.handle_application),
    path('apply/<str:custom_key>', views.UD_Apply.as_view()),

    # Update
    path('recru-profile/<int:pk>', views.U_RecruiterProfile.as_view()),

    # Update and Delete
    path('jobpost/<int:pk>', views.UD_JobPost.as_view()),
    path('test-one', views.job_posts),
]
