from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PhotographerProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Infos supplémentaires', {'fields': ('role', 'phone', 'avatar')}),
    )


@admin.register(PhotographerProfile)
class PhotographerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'plan', 'is_verified']
    list_filter = ['plan', 'is_verified']
    search_fields = ['user__username', 'city']