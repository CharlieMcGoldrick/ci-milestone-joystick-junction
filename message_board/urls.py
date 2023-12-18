from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account_management/', views.account_management, name='account_management'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('check_username_email', views.check_username_email, name='check_username_email'),
    path('logout/', views.logout_view, name='logout'),
]