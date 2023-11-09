from rest_framework.urls import path

from . import views

urlpatterns = [
    # Get and Post
    path('user/', views.G_Accounts.as_view()),
    path('posts/', views.G_Posts.as_view()),
    path('comments/', views.G_Comments.as_view()),

    # Update and Delete
    path('user/<int:pk>', views.UD_Accounts.as_view()),
    path('posts/<int:pk>', views.UD_Posts.as_view()),
    path('comments/<int:pk>', views.UD_Comments.as_view()),

    # Storing Files
    path('files/', views.G_Documents.as_view()),
    path('files/<int:pk>', views.U_Documents.as_view()),
    path('process-compatibility', views.G_TTGC.as_view()),
    path('process-recommendation', views.G_RPTG.as_view()),
]
