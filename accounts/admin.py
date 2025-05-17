from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserGroup


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for the custom User model."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'profile_picture', 'bio', 'phone_number')}),
        (_('Subscription'), {'fields': ('is_premium', 'subscription_end_date')}),
        (_('Preferences'), {'fields': ('preferred_curriculum', 'preferred_class_level')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_premium')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_premium', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    """Admin configuration for the UserGroup model."""

    list_display = ('name', 'group_type', 'admin', 'member_count', 'created_at')
    list_filter = ('group_type', 'created_at')
    search_fields = ('name', 'admin__email')
    filter_horizontal = ('members',)
    readonly_fields = ('created_at', 'updated_at')
