from django.contrib import admin, messages

from main_control.models import CustomUser
from .models import Subjects, Department, FacultyAdmin, Semester, Regulation, AssessmentType, Faculty, Batch
from django.contrib.auth.models import Group


class FAI(admin.StackedInline):
    model = FacultyAdmin
    can_delete = False
    verbose_name_plural = 'Faculty Admin'
    fk_name = 'department'  # This should refer to the ForeignKey field in FacultyAdmin
    extra = 0
    max_num = 1
    min_num = 1

class Faculty_Admin(admin.ModelAdmin):
    list_display = ['get_dpt_admin_username', 'get_department_name', ]
    search_fields = ['dpt_admin__user__username', 'department__name']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('department', 'dpt_admin', 'date_appointed'),
        }),
    )

    def get_dpt_admin_username(self, obj):
        return obj.dpt_admin.user.username

    get_dpt_admin_username.short_description = 'Department Admin Username'

    def get_department_name(self, obj):
        return obj.department.name

    get_department_name.short_description = 'Department Name'



    def save_model(self, request, obj, form, change):
        if not change:
            # If it's a new object, set the associated Faculty's faculty_type to 'Faculty Admin'
            obj.dpt_admin.faculty_type = 'Department Admin'
            obj.dpt_admin.save()

            # Add the user to the 'Faculty Admin' group
            faculty_admin_group, created = Group.objects.get_or_create(name='FacultyAdmin')
            obj.dpt_admin.user.groups.add(faculty_admin_group)

            super().save_model(request, obj, form, change)

            messages.success(request, f'{obj.dpt_admin.user.username} has been assigned as Faculty Admin successfully.')
        else:
            # If it's an existing object, handle group changes
            previous_instance = FacultyAdmin.objects.get(pk=obj.pk)
            previous_faculty = previous_instance.dpt_admin

            current_faculty = obj.dpt_admin
            if previous_faculty.faculty_type != current_faculty.faculty_type:
                # Remove the user from the old group if the previous faculty type was 'Faculty Admin'
                if previous_faculty.faculty_type == 'Department Admin':
                    old_group = Group.objects.filter(name='Faculty Admin').first()
                    if old_group:
                        previous_faculty.user.groups.remove(old_group)

                # Set the new faculty_type and update the user's group
                current_faculty.faculty_type = current_faculty.faculty_type
                current_faculty.save()

                new_group, created = Group.objects.get_or_create(name=current_faculty.faculty_type)
                current_faculty.user.groups.add(new_group)

            super().save_model(request, obj, form, change)

            messages.success(request, f'{current_faculty.user.username} has been updated successfully.')
    # inlines = [FAI]


class DepartmentAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('name', 'get_faculty_admin')
    # Fields to enable search functionality
    search_fields = ('name', 'description', )

    # Fieldsets to organize the detail view of the object
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
    )

    # Additional fieldsets to use when adding a new object
    add_fieldsets = (
        ('New Department', {
            'classes': ('wide',),
            'fields': ('name', 'description'),
        }),
    )

    def get_faculty_admin(self, obj):
        # Access the related FacultyAdmin object through the reverse relation
        faculty_admin = FacultyAdmin.objects.filter(department=obj).first()
        if faculty_admin:
            return faculty_admin.dpt_admin.user.name
        return 'No Admin Assigned'

    get_faculty_admin.short_description = 'Faculty Admin'

    # Optional: Specify the ordering of the fields in the list view
    ordering = ('name',)
    inlines = [FAI]
admin.site.register(Subjects)
admin.site.register(Department, DepartmentAdmin)
# admin.site.register(FacultyAdmin, Faculty_Admin)
admin.site.register(Semester)
admin.site.register(Regulation)
admin.site.register(AssessmentType)
admin.site.register(Batch)
