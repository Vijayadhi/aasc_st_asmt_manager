# from django.dispatch import receiver
# from django.contrib.auth.models import Group
# from .models import Faculty
# from django.db.models.signals import m2m_changed
#
#
# @receiver(m2m_changed, sender=Faculty.faculty_type.through)
# def assign_groups_to_user(sender, instance, action, **kwargs):
#     if action in ['post_add', 'post_remove', 'post_clear']:
#         # Clear all existing groups
#         instance.user.groups.clear()
#         print(instance.faculty_type)
#
#         # Assign groups based on faculty_type
#         for role in instance.faculty_type.all():
#             print(role)
#             group_name = role.name  # Assuming FacultyRoles has a 'name' field
#             print(group_name)
#             group, created = Group.objects.get_or_create(name=group_name)
#             instance.user.groups.add(group)
#
#         print(f"Groups have been assigned to {instance.user} based on their faculty types.")

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Faculty

@receiver(m2m_changed, sender=Faculty.faculty_type.through)
def manage_groups_for_user(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Define the relevant groups
        relevant_groups = {'Faculty', 'FacultyAdmin', 'Class Tutor'}

        # Clear only relevant groups (related to Faculty roles)
        user_groups = instance.user.groups.filter(name__in=relevant_groups)

        # Current faculty roles (faculty_type)
        current_roles = set(role.name for role in instance.faculty_type.all())

        # Remove groups not in the current roles
        for group in user_groups:
            if group.name not in current_roles:
                instance.user.groups.remove(group)
                print(f"Removed {group.name} from {instance.user}")

        # Add missing groups based on the current roles
        for role in current_roles:
            group, created = Group.objects.get_or_create(name=role)
            if group not in instance.user.groups.all():
                instance.user.groups.add(group)
                print(f"Added {group.name} to {instance.user}")

        print(f"Groups have been updated for {instance.user} based on their faculty types.")
