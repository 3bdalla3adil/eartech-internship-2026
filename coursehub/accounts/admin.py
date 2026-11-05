from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CourseHubUserAdmin(UserAdmin):
    """Expose the CourseHub role alongside Django's built-in user fields."""

    list_display = ("username", "email", "role", "is_staff", "is_superuser")
    list_filter = UserAdmin.list_filter + ("role",)
    fieldsets = UserAdmin.fieldsets + (
        ("CourseHub", {"fields": ("role",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("CourseHub", {"fields": ("role",)}),
    )
