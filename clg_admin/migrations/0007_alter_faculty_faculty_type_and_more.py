# Generated by Django 5.0.7 on 2024-08-19 20:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clg_admin', '0006_remove_faculty_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='faculty_type',
            field=models.CharField(choices=[('Department Admin', 'Department Admin'), ('Department Staff', 'Department Staff'), ('Class Tutor', 'Class Tutor')], default='Department Staff', max_length=20),
        ),
        migrations.AlterField(
            model_name='facultyadmin',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clg_admin.department'),
        ),
        migrations.AlterUniqueTogether(
            name='facultyadmin',
            unique_together={('dpt_admin', 'department')},
        ),
    ]
