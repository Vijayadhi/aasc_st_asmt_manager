from datetime import timedelta

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from main_control.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
def calculate_min_dob():
    # Users should not be older than 120 years
    return timezone.now().date() - timedelta(days=365 * 120)


def calculate_max_dob():
    # Users should be at least 18 years old
    return timezone.now().date() - timedelta(days=365 * 18)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=120, unique=False, null=True, blank=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255, unique=False)
    email = models.EmailField(_('email address'), unique=True)
    mobile_no = models.CharField(max_length=12, null=True, blank=True)
    blood_group = models.CharField(max_length=12, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_staff = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='media/faculty/%Y/%m/%d', null=True, blank=True)
    dob = models.DateField(null=True, blank=True, default=timezone.now,
                           help_text=f'eg. {str(timezone.now().date())}',
                           validators=[
                               MinValueValidator(calculate_min_dob()),
                               MaxValueValidator(calculate_max_dob())
                           ])
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['mobile_no']
    objects = CustomUserManager()

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = _('Manage Profile')
        verbose_name_plural = _('Manage Profiles')
        # db_table = 'main_custom_user'
