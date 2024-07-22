# Generated by Django 5.0.7 on 2024-07-20 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_control', '0002_alter_customuser_mobile_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_admin_user',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_faculty',
        ),
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='blood_group',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]
