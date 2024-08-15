from django.db import models
from django.contrib.auth.models import AbstractUser
from main_control.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _



# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=120)
    email = models.EmailField(_('email address'), unique=True)
    mobile_no = models.CharField(max_length=12, null=True, blank=True)
    blood_group = models.CharField(max_length=12, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'mobile_no']
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_model_perms(self, request):
        """
        Return empty perms dict for users who are not in a specific group.
        """
        perms = super().get_model_perms(request)

        # Custom logic based on user's group
        if request.user.groups.filter(name='CollegeAdmin').exists():
            self.verbose_name = _('Faculty Member (College Admin)')
            self.verbose_name_plural = _('Faculty Members (College Admin)')
        elif request.user.groups.filter(name='DepartmentAdmin').exists():
            self.verbose_name = _('Faculty Member (Dept Admin)')
            self.verbose_name_plural = _('Faculty Members (Dept Admin)')
        else:
            perms = {}  # Hide the model completely if the user doesn't belong to these groups

        return perms

    class Meta:
        verbose_name = _('Faculty Member')
        verbose_name_plural = _('Faculty')
