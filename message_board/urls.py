from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account_management/', views.account_management, name='account_management'),
    path('login/', views.login_view.as_view(template_name='account/login.html'), name='login'),
    path('signup/', views.signup_view, name='signup_view'),
    path('check_username_email', views.check_username_email, name='check_username_email'),
    path('search_games_for_main_thread/', views.search_games_for_main_thread, name='search_games_for_main_thread'),
    path('create_game_main_thread/<int:game_id>/', views.create_game_main_thread, name='create_game_main_thread'),
    path('search_created_main_threads/', views.search_created_main_threads, name='search_created_main_threads'),
    path('update_and_publish_thread/', views.update_and_publish_thread, name='update_and_publish_thread'),
    path('update_and_unpublish_thread/', views.update_and_unpublish_thread, name='update_and_unpublish_thread'),
    path('delete_a_main_thread/', views.delete_a_main_thread, name='delete_a_main_thread'),
    path('promote_to_admin/', views.promote_to_admin, name='promote_to_admin'),
    path('logout/', views.logout_view, name='logout'),
    path('homepage_search_threads/', views.homepage_search_threads, name='homepage_search_threads'),
    path('main_threads/<int:game_id>/', views.main_thread_detail, name='main_thread_detail'),
    path('post_comment/<int:game_id>/', views.post_comment, name='post_comment'),
    path('comment/<int:comment_id>/reply', views.reply_to_comment, name='reply_to_comment'),
    path('comment/<int:comment_id>/upvote', views.upvote_comment, name='upvote_comment'),
    path('comment/<int:comment_id>/downvote', views.downvote_comment, name='downvote_comment'),
    path('reply/<int:reply_id>/upvote', views.upvote_reply, name='upvote_reply'),
    path('reply/<int:reply_id>/downvote', views.downvote_reply, name='downvote_reply'),
]