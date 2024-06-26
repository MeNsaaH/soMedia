from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


# admin.site.register(User, UserAdmin)
class _structure(admin.ModelAdmin):
    list_display = ( "user","phone" , "address")
admin.site.register(UserProfile , _structure)