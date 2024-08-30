from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Students


@receiver(post_save, sender=Students)
def add_user_to_student_group(sender, instance, created, **kwargs):
    if created:
        # Get or create the Student group
        student_group, created = Group.objects.get_or_create(name='Student')

        # Add the user to the Student group
        instance.user.groups.add(student_group)
