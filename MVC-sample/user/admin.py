from django.contrib import admin
from user.models import UserProfile



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone', 'city', 'country', 'avatar_tag']

admin.site.register(UserProfile, UserProfileAdmin)