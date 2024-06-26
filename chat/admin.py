from django.contrib import admin

from .models import Comment, Post

class _comment_structure(admin.ModelAdmin):
    list_display=("user" , "text","comment_date" )

class _Post_structure(admin.ModelAdmin):
    list_display=("user" , "text","picture" )
admin.site.register(Comment , _comment_structure)
admin.site.register(Post , _Post_structure)