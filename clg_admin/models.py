from datetime import datetime

from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save, pre_save
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
        return self.user.name + ' - ' + self.faculty_type

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
    dpt_admin = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    date_appointed = models.DateField()

    def __str__(self):
        return self.dpt_admin.user.username + ' - ' + self.department.name

    class Meta:
        db_table = 'faculty_admin'
        unique_together = (('dpt_admin', 'department'),)

# @receiver(post_save, sender=FacultyAdmin)
# def assign_groups(sender, instance, created, **kwargs):
#     if created:
#         # Replace 'your_group_name' with the actual group names you want to assign
#         group_names = ['FacultyAdmin']  # List of group names to be assigned
#         faculty_instance = instance.dpt_admin
#         faculty_instance.faculty_type = 'Department Admin'
#         faculty_instance.save()
#
#
#         user = instance.dpt_admin.user  # Assuming `dpt_admin` is a `User` instance
#
#         for group_name in group_names:
#             group, created = Group.objects.get_or_create(name=group_name)
#             user.groups.add(group)

@receiver(pre_save, sender=FacultyAdmin)
def handle_faculty_admin_update(sender, instance, **kwargs):
    if instance.pk:
        # Fetch the previous instance to compare and handle changes
        previous_instance = FacultyAdmin.objects.get(pk=instance.pk)

        if previous_instance.dpt_admin != instance.dpt_admin:
            # Revert the old department admin back to 'Department Staff'
            old_faculty_instance = previous_instance.dpt_admin
            old_faculty_instance.faculty_type = 'Department Staff'
            old_faculty_instance.save()

            # Remove the old department admin from the 'FacultyAdmin' group
            old_group = Group.objects.get(name='FacultyAdmin')
            old_faculty_instance.user.groups.remove(old_group)

@receiver(post_save, sender=FacultyAdmin)
def assign_faculty_admin_group(sender, instance, created, **kwargs):
    faculty_instance = instance.dpt_admin

    if created:
        # If the instance is newly created, assign it as 'Department Admin'
        faculty_instance.faculty_type = 'Department Admin'
        faculty_instance.save()

        # Add the user to the 'FacultyAdmin' group
        group, _ = Group.objects.get_or_create(name='FacultyAdmin')
        faculty_instance.user.groups.add(group)
    else:
        # If updating an existing instance, ensure the current faculty instance is set as 'Department Admin'
        faculty_instance.faculty_type = 'Department Admin'
        faculty_instance.save()

        # Ensure the user is in the 'FacultyAdmin' group
        group, _ = Group.objects.get_or_create(name='FacultyAdmin')
        faculty_instance.user.groups.add(group)
        if not faculty_instance.user.groups.filter(name='FacultyAdmin').exists():
            pass



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
