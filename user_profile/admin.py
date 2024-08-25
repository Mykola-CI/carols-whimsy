from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Unregister the original User admin and register the new User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
