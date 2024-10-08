# Generated by Django 5.0.7 on 2024-08-29 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clg_admin', '0012_alter_facultyroles_name'),
        ('dept_admin', '0005_alter_facultyallocation_options'),
        ('dept_faculty', '0008_alter_addassessmentscore_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='addassessmentscore',
            unique_together={('subject', 'assessment', 'semester')},
        ),
        migrations.AddField(
            model_name='addassessmentscore',
            name='scores',
            field=models.JSONField(default=dict),
        ),
        migrations.RemoveField(
            model_name='addassessmentscore',
            name='score',
        ),
        migrations.RemoveField(
            model_name='addassessmentscore',
            name='student',
        ),
    ]
