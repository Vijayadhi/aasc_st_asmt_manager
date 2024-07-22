from django.db import models
from clg_admin.models import *
# Create your models here.
class Courses(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'courses'


class FacultyAllocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty.name} - {self.department.name}"

    class Meta:
        db_table = 'faculty_allocation'

class SubjectAllocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    faculty = models.ForeignKey(FacultyAllocation, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject.name} - {self.faculty.name} - {self.course.name}'
    class Meta:
        db_table = 'subject_allocation'



