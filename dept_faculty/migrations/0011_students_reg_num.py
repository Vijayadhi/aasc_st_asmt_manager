# Generated by Django 5.0.7 on 2024-08-29 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dept_faculty', '0010_scorestatus_addassessmentscore_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='reg_num',
            field=models.CharField(default='000', max_length=10),
            preserve_default=False,
        ),
    ]
