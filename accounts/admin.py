from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Office


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "email",
        "team",
        "is_staff",
    ]
    list_filter = ('team', "is_staff")
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("team",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("team",)}),)


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
