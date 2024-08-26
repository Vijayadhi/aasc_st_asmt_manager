from django.contrib import admin

from dept_faculty.models import Students, AddAssessmentScore


# Register your models here.
class StudentInline(admin.StackedInline):
    model = Students
    can_delete = False
    verbose_name_plural = 'Students'
    fk_name = 'user'
    extra = 0  # This prevents extra empty forms from being shown
    max_num = 1  # Limit to only one form
    min_num = 1  # Ensure that at least one form is displayed
admin.site.register(Students)
admin.site.register(AddAssessmentScore)