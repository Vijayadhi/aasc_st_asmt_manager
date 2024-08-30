from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from clg_admin.models import Faculty
from main_control.models import CustomUser


# Create your views here.
def createUser(request, user_email, mobile, user_name):
    try:
        if CustomUser.objects.filter(email=user_email, mobile_no=mobile).exists():
            return None, 'Email/Phone Number already registered'

        get_Groups = Group.objects.get(name='Faculty')
        user = CustomUser.objects.create_user(
            username=user_name,
            email=user_email,
            mobile_no=mobile,
            password="admin",
            is_staff=True,
            is_active=True
        )
        user.groups.add(get_Groups)
        print(user.id)
        print(get_Groups.user_set.all())
        return user, None  # No error

    except Exception as e:
        error_message = f'Error: {str(e)}'
        messages.error(request, error_message)
        return None, error_message
def user_logout(request):
    logout(request)
    return redirect('/login')

def find_user_group(email):
    user = CustomUser.objects.get(email=email)
    if user.groups.filter(name='College Admin').exists():
        return "clg_admin/admin_index"
    elif user.groups.filter(name='Department Admin').exists():
        return "dept_admin/dpt_admin_index"
    elif user.groups.filter(name='Department Faculty').exists():
        return "department faculty"
    elif user.groups.filter(name='Student').exists():
        return "student"


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')        # if
        password = request.POST.get('password')
        try:
            if username and password is not None:
                user = authenticate(username=username, password=password)
                user_group = find_user_group(username)
                print(username)
                print(user_group)
                if user is not None:
                    login(request, user)
                return redirect(f'{user_group}')
        except:
            raise ValueError("Enter Valid Username or Password")
    return render(request, 'backend/login.html')


@staff_member_required
def admin_dashboard(request):
    total_faculties = Faculty.objects.count()
    total_students = CustomUser.objects.filter(is_staff=False).count()

    context = {
        'total_faculties': total_faculties,
        'total_students': total_students,
    }
    return render(request, 'admin/dashboard.html', context)