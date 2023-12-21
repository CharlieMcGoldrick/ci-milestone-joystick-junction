from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account_management/', views.account_management, name='account_management'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup_view'),
    path('check_username_email', views.check_username_email, name='check_username_email'),
    path('search_games_for_main_thread/', views.search_games_for_main_thread, name='search_games_for_main_thread'),
    path('create_game_main_thread/<int:game_id>/', views.create_game_main_thread, name='create_game_main_thread'),
    path('search_created_main_threads/', views.search_created_main_threads, name='search_created_main_threads'),
    path('promote_to_admin/', views.promote_to_admin, name='promote_to_admin'),
    path('logout/', views.logout_view, name='logout'),
]