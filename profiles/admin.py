from django.contrib import admin
from .models import UserProfile, AvailableSlot

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'phone')  # Fields to display in the admin list view
    search_fields = ('name', 'email', 'phone')  # Fields to enable searching in the admin

@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'time', 'available')  # Fields to display in the admin list view
    list_filter = ('date', 'available')  # Fields to filter by in the admin
    search_fields = ('user__name', 'date')  # Fields to enable searching in the admin
