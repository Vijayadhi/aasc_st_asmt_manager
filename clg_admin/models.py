from datetime import datetime

from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from main_control.models import CustomUser


# Create your models here.

class Faculty(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joining_date = models.DateField()
    Faculty_Choices = [
        ('Department Admin', 'Department Admin'),
        ('Department Staff', 'Department Staff'),
        ('Class Tutor', 'Class Tutor'),
    ]
    major_study = models.CharField(max_length=200, null=True, blank=True)
    faculty_type = models.CharField(max_length=20, choices=Faculty_Choices, default='Department Staff')

    def __str__(self):
        return self.user.username + ' - ' + self.faculty_type

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
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    # department = models.OneToOneField(Department, on_delete=models.CASCADE)
    dpt_admin = models.OneToOneField(Faculty, on_delete=models.CASCADE)
    date_appointed = models.DateField()

    def __str__(self):
        return self.dpt_admin.user.username + ' - ' + self.department.name

    class Meta:
        db_table = 'faculty_admin'
        unique_together = (('dpt_admin', 'department'),)

@receiver(post_save, sender=FacultyAdmin)
def assign_groups(sender, instance, created, **kwargs):
    if created:
        # Replace 'your_group_name' with the actual group names you want to assign
        group_names = ['FacultyAdmin']  # Lis   t of group names to be assigned
        faculty_instance = instance.dpt_admin
        faculty_instance.faculty_type = 'Department Admin'
        user = instance.dpt_admin.user  # Assuming `dpt_admin` is a `User` instance

        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)




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
