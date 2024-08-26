from django.db import models
from urllib3 import request

from clg_admin.models import Department, AssessmentType, Batch
from dept_admin.models import Courses, SubjectAllocation
from main_control.models import CustomUser


# Create your models here.
class Students(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, blank=True, null=True, related_name='batch')
    # department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - {self.course.   department} - {self.course}"
    class Meta:
        db_table = 'students'
        verbose_name = 'Students'

class AddAssessmentScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    assessment = models.ForeignKey(AssessmentType, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    subject = models.ForeignKey(SubjectAllocation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student}"

    class Meta:
        db_table = 'add_assessment_score'
        unique_together = (('student', 'assessment',),)
