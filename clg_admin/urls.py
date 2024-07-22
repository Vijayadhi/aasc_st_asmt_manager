from django.urls import path

from clg_admin.views import add_faculty

urlpatterns = [
    path('add_faculty', add_faculty)
]