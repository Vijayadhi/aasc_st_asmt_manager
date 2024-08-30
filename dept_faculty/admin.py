from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse
from django.utils.html import format_html


from clg_admin.models import Faculty, Semester, AssessmentType
from dept_admin.models import SubjectAllocation
from dept_faculty.forms import AddAssessmentScoreForm
from dept_faculty.models import Students, AddAssessmentScore, ScoreStatus
from dept_faculty.views import generate_score_pdf


# Register your models here.
class StudentInline(admin.StackedInline):
    model = Students
    can_delete = False
    verbose_name_plural = 'Students'
    fk_name = 'user'
    extra = 0  # This prevents extra empty forms from being shown
    max_num = 1  # Limit to only one form
    min_num = 1  # Ensure that at least one form is displayed

class AddAssessmentScoreAdmin(admin.ModelAdmin):
    readonly_fields = ('display_scores',)
    add_form_template = 'dept_faculty/addScore.html'
    list_display_links = ('subject', 'assessment', 'semester',)
    change_list_template = 'dept_faculty/change_list.html'
    list_display = ('subject', 'assessment', 'semester', 'status_display', 'score_pdf_link')

    form = AddAssessmentScoreForm

    fieldsets = (
        ('Actions', {
            'fields': ('subject', 'assessment', 'semester', 'status')
        }),
        ('View MarkList', {
            'fields': ('display_scores',)
        }),
    )

    def status_display(self, obj):
        # Get the names of all related Status objects
        return ", ".join(status.name for status in obj.status.all())
    status_display.short_description = 'Status'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('list/', self.admin_site.admin_view(self.list_view), name='list_view'),
            path('custom-download/', self.admin_site.admin_view(self.custom_download_view),
                 name='custom_download_view'),
        ]
        return custom_urls + urls

    def list_view(self, request):
        # Custom logic for listing view
        context = self.get_custom_context(request)
        return render(request, 'dept_faculty/change_list.html', context)

    def custom_download_view(self, request):
        # Custom logic for download view
        context = self.get_custom_context(request)
        return render(request, 'dept_faculty/download_view.html', context)

    def get_custom_context(self, request):
        # Helper method to get context data
        current_user = request.user
        course_id = request.GET.get('course_id')
        batch_id = request.GET.get('batch_id')
        faculty_qs = Faculty.objects.filter(user=current_user)
        students = Students.objects.all()
        subjects_allocated = SubjectAllocation.objects.filter(faculty__in=faculty_qs)
        show_add_button = False  # Set to False to hide the Add button

        return {
            'students': students,
            'subjects_allocated': subjects_allocated,
            'course_id': course_id,
            'batch_id': batch_id,
            'show_add_button': show_add_button,
        }

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.get_custom_context(request))
        return super().changelist_view(request, extra_context=extra_context)

    def add_view(self, request, form_url="", extra_context=None):
        course_id = request.GET.get('course_id')
        batch_id = request.GET.get('batch_id')
        subject_id = request.GET.get('subject_id')
        std_reg_num = request.POST.getlist("std_reg_num")
        std_mark = request.POST.getlist("mark")
        assmt_type = request.POST.get("assmt_type")
        semester_data = request.POST.get("semester")

        # Debug print statements

        # Fetch related data for extra_context
        students = Students.objects.filter(batch__id=batch_id)
        semester = Semester.objects.all()
        assessment_type = AssessmentType.objects.all()

        extra_context = extra_context or {}
        extra_context['students'] = students
        extra_context['semester'] = semester
        extra_context['course_id'] = course_id
        extra_context['batch_id'] = batch_id
        extra_context['assessment_type'] = assessment_type

        # Initialize scores dictionary
        scores = {}

        for std_id, mark in zip(std_reg_num, std_mark):
            scores[std_id] = mark

        try:
            # Retrieve the related objects
            subject_instance = get_object_or_404(SubjectAllocation, id=subject_id)
            assessment_instance = get_object_or_404(AssessmentType, id=assmt_type)
            semester_instance = get_object_or_404(Semester, id=semester_data)



            # Create and save the AddAssessmentScore object
            add_score_data = AddAssessmentScore(
                subject=subject_instance,
                assessment=assessment_instance,
                semester=semester_instance,
                scores=scores  # Store the dictionary directly
            )
            add_score_data.save()
        except Exception as e:
            print(f"Failed to save data: {e}")

        # Pass extra_context to the form or perform custom logic
        return super().add_view(request, form_url, extra_context=extra_context)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form



    def display_scores(self, obj):
        scores = obj.scores  # This is the JSONField
        if not scores:
            return "No scores available"

        # Start building the HTML table
        html = """
        <table style='border: 1px solid #ccc; border-collapse: collapse;'>
            <tr>
                <th style='border: 1px solid black; padding: 5px;'>Student Name</th>
                <th style='border: 1px solid black; padding: 5px;'>Score</th>
            </tr>
        """

        for student_id, score in scores.items():
            try:
                student = Students.objects.get(reg_num=student_id)
                student_name = student.user.name  # Assuming the name field is in the related user model
            except Students.DoesNotExist:
                student_name = "Unknown Student"

            # Add rows to the table with student name and score
            html += f"""
            <tr>
                <td style='border: 1px solid black; padding: 5px;'>{student_name}</td>
                <td style='border: 1px solid black; padding: 5px;'>{score}</td>
            </tr>
            """

        html += "</table>"

        return format_html(html)

    display_scores.short_description = "Marks"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/pdf/', self.admin_site.admin_view(self.generate_pdf), name='generate_score_pdf'),
        ]
        return custom_urls + urls

    def generate_pdf(self, request, pk):
        return generate_score_pdf(request, pk)

    def score_pdf_link(self, obj):
        return format_html('<a class="button" href="{}">PDF</a>', reverse('admin:generate_score_pdf', args=[obj.pk]))

    score_pdf_link.short_description = 'Download PDF'
    score_pdf_link.allow_tags = True

admin.site.register(Students)
admin.site.register(AddAssessmentScore, AddAssessmentScoreAdmin)
admin.site.register(ScoreStatus)