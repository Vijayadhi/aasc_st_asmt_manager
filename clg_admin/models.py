
from django.db import models

from main_control.models import CustomUser


# Create your models here.
class FacultyRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    ROLE_CHOICES = [
        ('Faculty', 'Faculty'),
        ('FacultyAdmin', 'FacultyAdmin'),
        ('Class Tutor', 'Class Tutor'),
    ]
    name = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES, default='Department Staff')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'faculty_roles'


class Faculty(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joining_date = models.DateField()
    major_study = models.CharField(max_length=200, null=True, blank=True)
    faculty_type = models.ManyToManyField(FacultyRoles)

    def __str__(self):
        if self.id:  # Ensure the instance is saved
            roles = ", ".join([role.name for role in self.faculty_type.all()])
            return f"{self.user.name} - {roles}"
        else:
            return self.user.name

    class Meta:
        db_table = 'faculty'


class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'


class FacultyAdmin(models.Model):
    id = models.BigAutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, unique=True)
    dpt_admin = models.ForeignKey(Faculty, on_delete=models.CASCADE, unique=True)
    date_appointed = models.DateField()

    def __str__(self):
        return self.dpt_admin.user.name + ' - ' + self.department.name

    class Meta:
        db_table = 'faculty_admin'
        unique_together = ('dpt_admin', 'department')

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


class Regulation(
    models.Model):  # This class is added to define the regulations from the university for the courses based on subject. Ex. CBCS-2019
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

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

class LeaveLetter(models.Model):
    id = models.BigAutoField(primary_key=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    date = models.DateField()
    created = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.faculty.user.name} - {self.subject} - {self.date}"
    class Meta:
        db_table = 'leave_letter'