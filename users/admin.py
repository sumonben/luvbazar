from django.contrib import admin
from .models import UserProfile
# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'phone']
    # prepopulated_fields = {'slug': ('name',)}
