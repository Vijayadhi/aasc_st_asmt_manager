from audioop import error
from calendar import month

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from clg_admin.models import Faculty
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