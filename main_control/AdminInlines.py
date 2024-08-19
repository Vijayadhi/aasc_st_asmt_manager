from django.contrib import admin

from clg_admin.models import Faculty


class FacultyInline(admin.StackedInline):
    model = Faculty
    can_delete = False
    verbose_name_plural = 'Faculty'
    fk_name = 'user'
    extra = 0  # This prevents extra empty forms from being shown
    max_num = 1  # Limit to only one form
    min_num = 1  # Ensure that at least one form is displayed\