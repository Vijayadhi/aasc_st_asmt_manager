import logging
import sys

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from urllib3 import request

from clg_admin.admin import Faculty_Admin
from clg_admin.models import Faculty
from dept_faculty.admin import StudentInline
from main_control.adminHelper import get_fieldsets_for_user, get_inline_instances_for_user, \
    conditional_admin_registration
from main_control.forms import CustomUserCreationForm, CustomUserChangeForm
from main_control.models import CustomUser


# Register your models here.
# logger = "none"



# class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
#     # def get_list_display(self, request):
#     #     return get_custom_list_display(request)
#
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     fieldsets = (
#         (None, {'fields': ('email', 'password', 'username')}),
#         ('Personal', {'fields':('blood_group', 'address', 'dob', 'mobile_no')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#
#     )
#
#     add_fieldsets = (
#         ("Basic User Details", {
#             'classes': ('wide',),
#             'fields': (
#                 'email', 'username', 'mobile_no',
#             )
#         }),
#     )
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     # return qs.filter(is_superuser=False).select_related('student')  # Use select_related for performance
    #     return qs.filter(is_superuser=False)
#     #
#     # # def student_course_name(self, obj):
#     # #     # Retrieve the course name for the related students
#     # #     # Assumes each user has only one related student record
#     # #     student = obj.students.first()
#     # #     return student.course.name if student else None
#     # #
#     # # student_course_name.short_description = 'Course Name'
#     #
#     # def save_model(self, request, obj, form, change):
#     #     print(request.user)
#     #     if not change:
#     #         obj.set_password('admin')
#     #         obj.is_staff = True
#     #         obj.is_active = True
#     #     super().save_model(request, obj, form, change)
#     #
#     #     if request.user.groups.filter(name='College Admin').exists():
#     #         faculty_group, _ = Group.objects.get_or_create(name='Faculty')
#     #         obj.groups.add(faculty_group)
#     #
#     # def get_inline_instances(self, request, obj=None):
#     #     inline_instances = []
#     #     if request.user.groups.filter(name='College Admin').exists():
#     #         inline_instances.append(FacultyInline(self.model, self.admin_site))
#     #     elif request.user.groups.filter(name='Faculty').exists():
#     #         inline_instances.append(StudentInline(self.model, self.admin_site))
#     #     return inline_instances
#     #
#     # def changelist_view(self, request, extra_context=None):
#     #     extra_context = extra_context or {}
#     #     if request.user.groups.filter(name='College Admin').exists():
#     #         extra_context['title'] = _("Faculty Management")
#     #     elif request.user.groups.filter(name='Faculty').exists():
#     #         extra_context['title'] = _("Student Management")
#     #     return super().changelist_view(request, extra_context=extra_context)
#     #
#     # def change_view(self, request, object_id, form_url='', extra_context=None):
#     #     extra_context = extra_context or {}
#     #     if request.user.groups.filter(name='College Admin').exists():
#     #         extra_context['title'] = _("Faculty Details")
#     #     elif request.user.groups.filter(name='Faculty').exists():
#     #         extra_context['title'] = _("Student Details")
#     #     return super().change_view(request, object_id, form_url, extra_context=extra_context)
#     #
#     #

class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('name', 'email', 'faculty_type_display')
    list_filter = ('email', 'name',)
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        ("Basic Profile Details", {'fields': ('email', 'name')}),
        ("Personal Information", {'fields': ('blood_group', 'address', 'dob', 'mobile_no', 'groups')}),
        ("Permissions", {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        ("Basic Profile Details", {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile_no', 'groups'),
        }),
    )

    def faculty_type_display(self, obj):
        """
        Display the faculty_type from the related Faculty model.
        """
        faculty = Faculty.objects.filter(user=obj).first()
        return faculty.faculty_type if faculty else 'Not Assigned'

    faculty_type_display.short_description = 'Faculty Type'

    def get_fieldsets(self, request, obj=None):
        return get_fieldsets_for_user(super().get_fieldsets, request, obj)

    def get_inline_instances(self, request, obj=None):
        if obj is None:  # obj is None when creating a new object
            return get_inline_instances_for_user(self, request, obj)
        return []  # Return an empty list when editing an existing object

    def save_model(self, request, obj, form, change):
        print(request.user)
        if not change:
            obj.set_password('admin')
            # obj.is_staff = True
            # obj.is_active = True
        super().save_model(request, obj, form, change)

        if request.user.groups.filter(name='College Admin').exists():
            faculty_group, _ = Group.objects.get_or_create(name='Faculty')
            obj.groups.add(faculty_group)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        current_user = request.user

        if current_user.groups.filter(name='College Admin').exists():
            # If the current user is in the College Admin group, show users in the Faculty group
            # admin.site.unregister(CustomUser)
            faculty_group = Group.objects.get(name='Faculty')
            return queryset.filter(groups=faculty_group)

        elif current_user.groups.filter(name='FacultyAdmin').exists():
            # If the current user is in the Faculty Admin group, show users in the Faculty group
            faculty_group = Group.objects.get(name='Faculty')
            return queryset.filter(groups=faculty_group)

        elif current_user.groups.filter(name='Class Tutor').exists():
            # If the current user is in the Class Tutor group, show users in the Student group
            student_group = Group.objects.get(name='Student')
            return queryset.filter(groups=student_group)

        elif current_user.groups.filter(name='Faculty').exists():
            # If the current user is in the Class Tutor group, show users in the Student group
            # student_group = Group.objects.get(name='Student')
            # return queryset.filter(groups=student_group)
            admin.site.unregister(CustomUser)


        else:
            # Otherwise, return an empty queryset or handle as needed
            return queryset




    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     # return qs.filter(is_superuser=False).select_related('student')  # Use select_related for performance
    #     return qs.filter(is_superuser=False)
    jazzmin_section_order = ("Basic Profile Details", "Personal Information", "Permissions")


class MyAdminSite(admin.AdminSite):
    site_header = _('My Admin Site')

    def each_context(self, request):
        # Call the conditional registration function
        if request.user.is_authenticated:
            conditional_admin_registration(request.user)
        return super().each_context(request)

admin_site = MyAdminSite(name='myadmin')


admin.site.register(CustomUser, CustomUserAdmin)
