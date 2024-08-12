from django.urls import path

from clg_admin.views import add_faculty, admin_index, add_department

urlpatterns = [
    path('add_faculty', add_faculty),
    path('admin_index', admin_index),
    path('add_department', add_department)
]
