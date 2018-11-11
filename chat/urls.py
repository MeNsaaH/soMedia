""" soMedia URL Configuration """

from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.home, name='home'),
    path('posts/add', views.add_post, name='add_post'),
    path('comments/add/<post_id>', views.add_comment, name='add_comment')
]
