from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'age')}),
    )

    # Show custom fields in the list display
    list_display = ('email', 'role', 'phone_number', 'age', 'is_staff', 'is_active')

    # Add filters for role and is_staff
    list_filter = ('role', 'is_staff', 'is_active')

    # Add search functionality
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')

admin.site.register(CustomUser, CustomUserAdmin)
