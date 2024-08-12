from django.urls import path
from dept_admin.views import *

urlpatterns = [
    path('dpt_admin_index', dpt_admin_index, name='dpt_admin_index'),
]