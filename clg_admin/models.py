from datetime import datetime

from django.db import models

from main_control.models import CustomUser


# Create your models here.

class Faculty(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joining_date = models.DateField()
    Faculty_Choices = [
        ('Department Admin', 'Department Admin'),
        ('Department Staff', 'Department Staff'),
    ]
    major_study = models.CharField(max_length=200, null=True, blank=True)
    faculty_type = models.CharField(max_length=20, choices=Faculty_Choices, default='Department Staff')
    photo = models.ImageField(upload_to='media/faculty/%Y/%m/%d', null=True, blank=True)
    def __str__(self):
        return self.user.username + ' - ' + self.faculty_type

    class Meta:
        db_table = 'faculty'

class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'

class FacultyAdmin(models.Model):
    id = models.BigAutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    dpt_admin = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    date_appointed = models.DateField()

    def __str__(self):
        return self.dpt_admin.user.name + ' - ' + self.department.name

    class Meta:
        db_table = 'faculty_admin'

class Batch(models.Model):
    id = models.BigAutoField(primary_key=True)
    batch_from_date = models.IntegerField()
    batch_to_date = models.IntegerField()

    def __str__(self):
        return f'{self.batch_from_date} - {self.batch_to_date}'
    class Meta:
        db_table = 'batch'

class Semester(models.Model):
    id = models.BigAutoField(primary_key=True)
    semester = models.CharField(max_length=200, null=True, blank=True, unique=True)

    def __str__(self):
        return self.semester
    class Meta:
        db_table = 'semester'

class Regulation(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'regulation'

class Subjects(models.Model):
    id = models.BigAutoField(primary_key=True)
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'subjects'


class AssessmentType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'assessment_type'



