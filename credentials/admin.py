from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group


class ProfileAdmin(UserAdmin):
    form = UserChangeForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                )
            },
        ),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}),
        ("User info", {"fields": ("contact_no",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "contact_no",
        "get_date_joined",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    list_filter = ["is_active", "is_staff"]

    filter_horizontal = []

    def get_date_joined(self, obj):
        return obj.date_joined


admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(Group)
