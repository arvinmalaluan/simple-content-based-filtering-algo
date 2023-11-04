from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login', views.login, name='authenticate'),
    path('register', views.register, name='register'),
    path('update-password', views.update_user_info, name='changepass'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('info', views.get_user_info),
    path('info/<int:pk>', views.getAccount.as_view()),
    path('all-info', views.get_all_info),

]
