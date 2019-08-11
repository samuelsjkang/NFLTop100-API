from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from main import models


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['name', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
