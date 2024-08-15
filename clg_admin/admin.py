from django.contrib import admin, messages

from .models import Faculty, Subjects, Department, FacultyAdmin, Semester, Regulation, AssessmentType
from django.contrib.auth.models import Group


class Faculty_Admin(admin.ModelAdmin):
    list_display = ['user', 'faculty_type', 'joining_date']
    search_fields = ['user__username', 'department__name']

    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         # If it's a new object, set faculty_type to 'Department Admin'
    #         obj.faculty_type = 'FacultyAdmin'

        # Ensure the user's group is updated based on the faculty_type
        # if obj.pk:
        #     # Update the group if the faculty_type changes
        #     previous_instance = Faculty.objects.get(pk=obj.pk)
        #     if previous_instance.faculty_type != obj.faculty_type:
        #         old_group = Group.objects.filter(name=previous_instance.faculty_type).first()
        #         if old_group:
        #             previous_instance.user.groups.remove(old_group)
        #
        # # Ensure the new group is assigned
        # new_group, created = Group.objects.get_or_create(name=obj.faculty_type)
        # obj.user.groups.add(new_group)

        # Save the Faculty object
        # obj.save()
        # messages.success(request, f'{obj.user.username} has been updated successfully')# admin.site.register(Faculty, Faculty_Admin)
admin.site.register(Subjects)
admin.site.register(Department)
admin.site.register(FacultyAdmin)
admin.site.register(Semester)
admin.site.register(Regulation)
admin.site.register(AssessmentType)

