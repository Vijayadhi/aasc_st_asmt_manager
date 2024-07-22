from django.contrib import admin, messages

from .models import Faculty

class FacultyAdmin(admin.ModelAdmin):
    list_display = ['user', 'faculty_type', 'joining_date']
    search_fields = ['user__username', 'department__name']

    def save_model(self, request, obj, form, change):
        if change:
            # Check if the department admin is being changed
            if 'faculty_type' in form.changed_data and obj.faculty_type == 'Department Admin':
                previous_admins = Faculty.objects.filter(department=obj.department, faculty_type='Department Admin')
                for prev_admin in previous_admins:
                    prev_admin.faculty_type = 'Department Staff'
                    prev_admin.save()

        obj.save()
        messages.success(request, f'{obj.user.username} has been updated successfully')

admin.site.register(Faculty, FacultyAdmin)