# Generated by Django 5.0.7 on 2024-08-29 17:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clg_admin', '0012_alter_facultyroles_name'),
        ('dept_admin', '0005_alter_facultyallocation_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subjectallocation',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='subjectallocation',
            name='semester',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='clg_admin.semester'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='subjectallocation',
            unique_together={('subject', 'course', 'batch', 'faculty', 'semester')},
        ),
    ]
