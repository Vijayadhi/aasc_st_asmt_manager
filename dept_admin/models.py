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
        unique_together = (('name', 'department'),)


class FacultyAllocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty.user.name} - {self.department.name}"

    class Meta:
        db_table = 'faculty_allocation'
        unique_together = (('faculty', 'department', 'course', 'batch'),)

@receiver(pre_save, sender=FacultyAllocation)
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

@receiver(post_save, sender=FacultyAllocation)
def assign_faculty_admin_group(sender, instance, created, **kwargs):
    faculty_instance = instance.faculty

    if created:
        # If the instance is newly created, assign it as 'Department Admin'
        faculty_instance.faculty_type = 'Class Tutor'
        faculty_instance.save()

        # Add the user to the 'FacultyAdmin' group
        group, _ = Group.objects.get_or_create(name='Class Tutor')
        faculty_instance.user.groups.add(group)
    else:
        # If updating an existing instance, ensure the current faculty instance is set as 'Department Admin'
        faculty_instance.faculty_type = 'Class Tutor'
        faculty_instance.save()

        # Ensure the user is in the 'FacultyAdmin' group
        group, _ = Group.objects.get_or_create(name='Class Tutor')
        faculty_instance.user.groups.add(group)
        if not faculty_instance.user.groups.filter(name='Class Tutor').exists():
            pass

class SubjectAllocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    # department = models.ForeignKey(Department, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject.name} - {self.faculty.user.name} - {self.course.name}'
    class Meta:
        db_table = 'subject_allocation'
        unique_together = (('subject', 'course', 'batch'),)



