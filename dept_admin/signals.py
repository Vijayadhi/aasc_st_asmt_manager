from django.db.models.signals import post_save
from django.dispatch import receiver

from clg_admin.models import Faculty, FacultyRoles
from dept_admin.models import FacultyAllocation


@receiver(post_save, sender=FacultyAllocation)
def update_faculty_role_for_current_user(sender, instance, created, **kwargs):
    current_user = instance.faculty.user  # Assuming `faculty` is the current faculty
    faculty = Faculty.objects.get(user=current_user)

    if created or faculty == instance.faculty:
        class_tutor_role, created = FacultyRoles.objects.get_or_create(name='Class Tutor')

        # Update the faculty_type for the current faculty
        faculty.faculty_type.add(class_tutor_role)
        faculty.save()
        print(f"Added 'Class Tutor' role to {faculty.user.username}")
