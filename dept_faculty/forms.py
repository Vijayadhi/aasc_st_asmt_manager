from django import forms
from .models import AddAssessmentScore, Students, Courses, Batch, SubjectAllocation

class AssessmentSelectionForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Courses.objects.all())
    batch = forms.ModelChoiceField(queryset=Batch.objects.all())
    subject = forms.ModelChoiceField(queryset=SubjectAllocation.objects.all())

class AddAssessmentScoreForm(forms.ModelForm):
    class Meta:
        model = AddAssessmentScore
        fields = ['assessment', 'semester', 'scores']

    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students', [])
        super(AddAssessmentScoreForm, self).__init__(*args, **kwargs)
        for student in students:
            self.fields[f'student_{student.id}'] = forms.IntegerField(
                label=student.user.name, initial=0, required=True
            )
