from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account_management/', views.account_management, name='account_management'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup_view'),
    path('check_username_email', views.check_username_email, name='check_username_email'),
    path('logout/', views.logout_view, name='logout'),
]