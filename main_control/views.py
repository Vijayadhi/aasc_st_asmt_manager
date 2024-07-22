from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

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

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponse('Logged In')
    return render(request, 'backend/login.html')