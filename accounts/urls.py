""" accounts URL Configuration """

from django.urls import path, include
from . import views


app_name = 'accounts'
urlpatterns = [
	path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('followers/', views.followers, name='followers'),
    path('my-profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<username>/', views.profile, name='view-profile'),
    path('users/follow/<username>/', views.follow, name='follow'),
    path('users/unfollow/<username>/', views.unfollow, name='unfollow'),
]
