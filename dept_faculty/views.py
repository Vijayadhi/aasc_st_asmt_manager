from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.templatetags.static import static
from xhtml2pdf import pisa

from dept_faculty.models import Students, AddAssessmentScore




def render_to_pdf(template_src, context_dict={}):
    template = render_to_string(template_src, context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="score_report.pdf"'
    pisa_status = pisa.CreatePDF(template, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + template + '</pre>')
    return response


def generate_score_pdf(request, pk):
    score = get_object_or_404(AddAssessmentScore, pk=pk)

    # Extract student reg_nums from the scores dictionary
    student_reg_nums = score.scores.keys()

    # Query the Students model based on reg_nums
    students = Students.objects.filter(reg_num__in=student_reg_nums)

    # Create a dictionary mapping reg_num to student names
    students_dict = {student.reg_num: student.user.name for student in students}

    logo_url = request.build_absolute_uri(static('backend/assets/img/img.png'))



    # Prepare context for rendering the PDF
    context = {
        'course': score.subject.course,
        'batch': score.subject.batch,
        'subject': score.subject,
        'assessment': score.assessment,
        'semester': score.semester,
        'scores': score.scores,
        'student_dict': students_dict,
        'logo_url': logo_url,
        'month_year': score.month,
    }

    return render_to_pdf('dept_faculty/internal_pdf_template.html', context)
