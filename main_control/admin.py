from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from clg_admin.admin import Faculty_Admin
from clg_admin.models import Faculty
from main_control.forms import CustomUserCreationForm, CustomUserChangeForm
from main_control.models import CustomUser


# Register your models here.

class FacultyInline(admin.StackedInline):
    model = Faculty
    can_delete = False
    verbose_name_plural = 'Faculty'
    fk_name = 'user'
    extra = 0  # This prevents extra empty forms from being shown
    max_num = 1  # Limit to only one form
    min_num = 1  # Ensure that at least one form is displayed


class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ('email', 'username')
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    inlines = (FacultyInline,)  # Include the Faculty inline form
    jazzmin_section_order = ("Basic User Details", "Faculty Details")

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal', {'fields':
                             ('blood_group', 'address', 'dob', 'mobile_no'
                              )}
         ),
    )

    add_fieldsets = (
        ("Basic User Details", {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'mobile_no',
            )
        }),
    )

    # def get_groups(self, obj):
    #     return ", ".join(group.name for group in obj.groups.all())

    # get_groups.short_description = 'Groups'

    # def changelist_view(self, request, extra_context=None):
    #     if extra_context is None:
    #         extra_context = {}
    #     # Pass current user to the template context
    #     extra_context['current_user'] = request.user
    #     return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False,  )

    # index_title = 'College Admin Dashboard'

    def save_model(self, request, obj, form, change):
        # Set the default password and staff status when creating a new user
        if not change:
            obj.set_password('admin')
            obj.is_staff = True
            obj.is_active = True
        super().save_model(request, obj, form, change)

        # Check if the user who is creating this user is in the "College Admin" group
        if request.user.groups.filter(name='College Admin').exists():
            faculty_group, created = Group.objects.get_or_create(name='Faculty')
            obj.groups.add(faculty_group)
            # Automatically create Faculty object if the user is created by a "College Admin"
            # if not change:
            #     Faculty.objects.create(
            #         user=obj,
            #         faculty_type='Department Staff'  # Default type; customize as needed
            #
            #     )
            #     self.message_user(request, f'Faculty profile created for {obj.username}', level='success')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Faculty, Faculty_Admin)
