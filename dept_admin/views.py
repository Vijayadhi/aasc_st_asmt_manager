from django.shortcuts import render

# Create your views here.
def dpt_admin_index(request):
    return render(request, 'dept_admin/dpt_admin_index.html')