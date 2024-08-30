from django.contrib.auth.models import Group
from django.db import models

from clg_admin.models import Department, AssessmentType, Batch, Semester
from dept_admin.models import Courses, SubjectAllocation
from main_control.models import CustomUser


# Create your models here.
class Students(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student')
    reg_num = models.CharField(max_length=10, unique=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, blank=True, null=True, related_name='batch')
    # department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - {self.course.   department} - {self.course}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        student_group, created = Group.objects.get_or_create(name='Student')
        self.user.groups.add(student_group)
        print("Successfully saved student group")

    class Meta:
        db_table = 'students'
        verbose_name = 'Students'

# class AddAssessmentScore(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     student = models.ForeignKey(Students, on_delete=models.CASCADE)
#     assessment = models.ForeignKey(AssessmentType, on_delete=models.CASCADE)
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
#     score = models.IntegerField(default=0)
#     subject = models.ForeignKey(SubjectAllocation, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"{self.student}"
#
#     class Meta:
#         db_table = 'add_assessment_score'
#         unique_together = (('student', 'assessment', 'subject', 'semester'),)

class ScoreStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=35, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'scorestatus'

class AddAssessmentScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(SubjectAllocation, on_delete=models.CASCADE)
    assessment = models.ForeignKey(AssessmentType, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    status = models.ManyToManyField(ScoreStatus)
    month = models.CharField(max_length=50, default="September - 2024")
    scores = models.JSONField(default=dict)  # Stores scores in a JSON format like {"student_id": score}

    def __str__(self):
        return f"{self.subject} - {self.assessment} - {self.semester} - {self.status}"

    class Meta:
        db_table = 'add_assessment_score'
        unique_together = (('subject', 'assessment', 'semester'),)
        verbose_name = 'Generate MarkList'
