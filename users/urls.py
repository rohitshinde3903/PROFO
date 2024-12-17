from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'), 
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/followers/', views.view_followers, name='view_followers'),
    path('profile/<str:username>/following/', views.view_following, name='view_following'),
    path('social-links/', views.social_links, name='social_links'),  # Specific pattern
    path('social-link/<int:link_id>/track/', views.track_social_link, name='track_social_link'),
    path('social-links/edit/<int:link_id>/', views.edit_social_link, name='edit_social_link'),
    path('social-links/delete/<int:link_id>/', views.delete_social_link, name='delete_social_link'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_profiles, name='search_profiles'),
    path('track-link/<int:link_id>/', views.track_social_link, name='track_social_link'),
    path('click/<int:link_id>/', views.track_click, name='track_click'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('notifications/', views.notifications, name='notifications'),
    path('<str:username>/', views.public_profile, name='public_profile'),  # Generic pattern
]

