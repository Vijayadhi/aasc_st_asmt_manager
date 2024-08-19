# Generated by Django 5.0.7 on 2024-08-19 14:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clg_admin', '0005_alter_facultyadmin_department_and_more'),
        ('dept_admin', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dept_admin.courses')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clg_admin.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Students',
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='AddAssessmentScore',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(default=0)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clg_admin.assessmenttype')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dept_faculty.students')),
            ],
            options={
                'db_table': 'add_assessment_score',
                'unique_together': {('student', 'assessment')},
            },
        ),
    ]
