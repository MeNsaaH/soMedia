from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.home, name='home'),
    path('posts/add', views.add_post, name='add_post'),
    path('comments/add/<int:post_id>', views.add_comment, name='add_comment'),
    path('posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('posts/search', views.search_posts, name='search_posts'),  # New URL pattern for search
]
