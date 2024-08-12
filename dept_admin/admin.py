from django.contrib import admin

from .models import FacultyAllocation, Courses, SubjectAllocation

# Register your models here.
admin.site.register(FacultyAllocation)
admin.site.register(Courses)
admin.site.register(SubjectAllocation)
