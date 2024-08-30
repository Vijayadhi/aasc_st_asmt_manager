from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Faculty, FacultyAdmin
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver

from clg_admin.models import Faculty, FacultyRoles

@receiver(m2m_changed, sender=Faculty.faculty_type.through)
def assign_groups_to_user(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Clear all existing groups
        instance.user.groups.clear()

        # Assign groups based on faculty_type
        for role in instance.faculty_type.all():
            group_name = role.name  # Assuming FacultyRoles has a 'name' field
            group, created = Group.objects.get_or_create(name=group_name)
            instance.user.groups.add(group)

        print(f"Groups have been assigned to {instance.user} based on their faculty types.")


@receiver(post_save, sender=FacultyAdmin)
def update_faculty_role_for_current_user(sender, instance, created, **kwargs):
    current_user = instance.dpt_admin.user  # Assuming `faculty` is the current faculty
    faculty = Faculty.objects.get(user=current_user)

    if created or faculty == instance.faculty:
        class_tutor_role, created = FacultyRoles.objects.get_or_create(name='FacultyAdmin')

        # Update the faculty_type for the current faculty
        faculty.faculty_type.add(class_tutor_role)
        faculty.save()
        print(f"Added 'Class Tutor' role to {faculty.user.username}")
