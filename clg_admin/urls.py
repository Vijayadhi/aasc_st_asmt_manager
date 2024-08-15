from django.urls import path

from clg_admin.views import add_faculty, admin_index, add_department, add_regulations, add_subject, manage_department, \
    test_index

urlpatterns = [
    path('add_faculty', add_faculty, name='add_faculty'),
    path('admin_index', admin_index, name='admin_index'),
    path('add_department', add_department, name="add_department"),
    path('manage_department', manage_department, name="manage_department"),
    path('add_regulations', add_regulations, name='add_regulations'),
    path('add_subjects', add_subject, name='add_subject'),
    path('test_index', test_index, name='test_index')
]
