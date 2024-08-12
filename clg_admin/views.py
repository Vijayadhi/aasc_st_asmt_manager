from audioop import error
from calendar import month

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from clg_admin.models import Faculty, Department, Regulation
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
        print(mobile_no, user)
        return HttpResponse("User created successfully")

    return render(request, 'clg_admin/add_faculty.html')

def admin_index(request):
    return render(request, 'clg_admin/admin_index.html')


def add_department(request):
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
        return redirect('/add_department')  # Redirect to an appropriate view after success

    return render(request, "clg_admin/add_department.html")

def add_regulations(request):
    if request.method == "POST":
        regulation_name = request.POST.get('regulation_name')
        print(regulation_name)
        if regulation_name == "":
            error_message = f'Error: Regulation "{regulation_name}" should not empty.'
            messages.error(request, error_message)
            return render(request, "clg_admin/add_regulations.html", {'error_message': error_message})

        print(regulation_name)

        # Check if the department name already exists
        department_exists = Regulation.objects.filter(name=regulation_name).exists()
        if department_exists:
            error_message = f'Error: Regulation "{regulation_name}" already exists.'
            messages.error(request, error_message)
            return render(request, "clg_admin/add_regulations.html", {'error_message': error_message})

        # Create a new department if it doesn't exist
        new_dregulation = Regulation(name=regulation_name)
        new_dregulation.save()

        success_message = f'Regulation "{regulation_name}" has been successfully created.'
        messages.success(request, success_message)
        return render(request, "clg_admin/add_regulations.html")  # Redirect to an appropriate view after success


    return render(request, "clg_admin/add_regulations.html")