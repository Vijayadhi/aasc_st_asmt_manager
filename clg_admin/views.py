from django.contrib import messages
from django.shortcuts import render, redirect

from clg_admin.models import Faculty, Department, Regulation, Subjects, FacultyAdmin
from main_control.views import createUser


# Create your views here.
def add_faculty(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('user_name')
        mobile_no = request.POST.get('mobile')
        date = request.POST.get('date')
        print(mobile_no)

        user, error = createUser(request, email, mobile_no, username)

        if error:
            print(error)
            messages.error(request, error)
            return render(request, 'clg_admin/add_faculty.html')  # Re-render the form with errors

        # Creating the Faculty Profile
        add_faculty_data = Faculty(
            user=user,
            joining_date=date
        )
        add_faculty_data.save()

        success_message = f'User "{username}" has been successfully created.'
        messages.success(request, success_message)
        return redirect('add_faculty')
    return render(request, 'clg_admin/add_faculty.html',)

def admin_index(request):
    return render(request, 'clg_admin/admin_index.html')


def add_department(request):
    departments = Department.objects.all()
    if request.method == "POST":
        dpt_name = request.POST.get('dpt_name')
        dpt_desc = request.POST.get('dpt_desc')
        print(dpt_name)
        print(dpt_desc)

        # Check if the department name already exists
        department_exists = Department.objects.filter(name=dpt_name).exists()
        if department_exists:
            error_message = f'Error: Department "{dpt_name}" already exists.'
            messages.error(request, error_message)
            return render(request, "clg_admin/add_department.html", {'error_message': error_message})

        # Create a new department if it doesn't exist
        new_department = Department(name=dpt_name, description=dpt_desc)
        new_department.save()

        success_message = f'Department "{dpt_name}" has been successfully created.'
        messages.success(request, success_message)
        return redirect('add_department')  # Redirect to an appropriate view after success

    return render(request, "clg_admin/add_department.html", {"departments": departments})
def manage_department(request):
    department = Department.objects.all()
    dpt_faculties = Faculty.objects.filter(faculty_type="Department Staff")
    dpt_admin = FacultyAdmin.objects.all()
    context = {'departments': department, 'dpt_faculties': dpt_faculties, 'dpt_admin': dpt_admin}
    return render(request, 'clg_admin/manage_department.html', context)


def add_regulations(request):
    if request.method == "POST":
        regulation_name = request.POST.get('regulation_name')
        print(regulation_name)
        if regulation_name == "":
            error_message = f'Error: Regulation "{regulation_name}" should not empty.'
            messages.error(request, error_message)
            return render(request, "clg_admin/add_regulations.html", {'error_message': error_message})


        # Check if the department name already exists
        department_exists = Regulation.objects.filter(name=regulation_name).exists()
        if department_exists:
            error_message = f'Error: Regulation "{regulation_name}" already exists.'
            messages.error(request, error_message)
            return render(request, "clg_admin/add_regulations.html", {'error_message': error_message})

        # Create a new department if it doesn't exist
        new_regulation = Regulation(name=regulation_name)
        new_regulation.save()

        success_message = f'Regulation "{regulation_name}" has been successfully created.'
        messages.success(request, success_message)
        return redirect('add_regulations')

    regulations = Regulation.objects.all()
    return render(request, "clg_admin/add_regulations.html", {'regulations': regulations})


def add_subject(request):
    if request.method == "POST":
        sub_name = request.POST.get('sub_name')
        regulation_id = request.POST.get('regulation')
        regulation = Regulation.objects.get(id=regulation_id)

        # Save the new subject here...
        if sub_name and regulation_id == "":
            error_message = f'Error: Subject Name and the Regulation should not empty.'
            messages.error(request, error_message)
            return render(request, "clg_admin/add_subjects.html", {'error_message': error_message})

        # Add success message
        new_subjects = Subjects(name=sub_name, regulation=regulation)
        new_subjects.save()
        messages.success(request, 'Subject created successfully!')
        return redirect('add_subject')

    regulations = Regulation.objects.all()
    subjects = Subjects.objects.all()
    context = {'regulations': regulations, 'subjects': subjects}
    return render(request, 'clg_admin/add_subjects.html', context)


def test_index(request):
    return render(request, 'clg_admin/test.html')