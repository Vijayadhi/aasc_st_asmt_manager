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

