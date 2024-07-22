from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main_control.forms import CustomUserCreationForm, CustomUserChangeForm
from main_control.models import CustomUser


# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('email',)
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Permissions', {'fields':
                             ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
                              'blood_group', 'address', 'dob', 'mobile_no'
                              )}
         ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'mobile_no',
                'password1', 'password2', 'is_active',
                'is_staff', 'is_superuser', 'groups',
                'user_permissions', 'blood_group', 'address', 'dob'
            )
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)