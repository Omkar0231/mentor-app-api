from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , OTPVerification

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'created_at')
    search_fields = ('email', 'otp')


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "first_name", "last_name", "role", "password", "is_staff", "is_superuser" )
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "role", "age")}),   
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "role", "is_staff", "is_superuser", "is_active"),
        }),
    )

    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)  # Change from 'username' to 'email'

admin.site.register(CustomUser, CustomUserAdmin)

