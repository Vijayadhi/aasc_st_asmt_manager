# from django.contrib import admin
#
# from dept_faculty.admin import StudentInline
# from dept_faculty.models import Students
# from main_control.models import CustomUser
#
#
# def get_custom_list_display(request):
#     if request.user.groups.filter(name='College Admin').exists():
#         return 'email', 'username',
#     elif request.user.groups.filter(name='Faculty').exists():
#         # admin.site.register(Students)
#         # admin.site.unregister(CustomUser)
#         return 'email', 'username'
#     return ('email',)  # Default list display
#
#
# from clg_admin.admin import BatchInline
from dept_faculty.admin import StudentInline
from .AdminInlines import FacultyInline


def get_fieldsets_for_user(super_func, request, obj=None):
    if request.user.groups.filter(name='College Admin').exists():
        # Fieldsets for College Admins
        fieldsets = [
            ('Basic Profile Details', {'fields': ('email', 'name')}),
        ]

        # Display "Personal Information" only when the logged-in user is viewing their own profile
        if obj is not None and obj == request.user:
            fieldsets.append(
                ("Personal Information", {'fields': ('blood_group', 'address', 'dob', 'mobile_no', 'photo')}))

        return fieldsets

    elif request.user.groups.filter(name='Faculty').exists():
        # Fieldsets for Faculty
        return (
            ('Basic Profile Details', {'fields': ('email', 'name')}),

            # Uncomment the following line if you want to show Personal Information for Faculty
            # ("Personal Information", {'fields': ('mobile_no', 'blood_group', 'address', 'dob', 'photo')}),
        )

    else:
        # Default fieldsets for other users
        return super_func(request, obj)


# def get_user_inline_instances(self, request, obj=None):
#     inline_instances = []
#     if request.user.groups.filter(name='College Admin').exists():
#         inline_instances.append(FacultyInline(self.model, self.admin_site))
#     elif request.user.groups.filter(name='Class Tutor').exists():
#         inline_instances.append(StudentInline(self.model, self.admin_site))
#     return inline_instances

def get_inline_instances_for_user(admin_class, request, obj=None):
    inline_instances = []
    if request.user.groups.filter(name='College Admin').exists():
        inline_instances.append(FacultyInline(admin_class.model, admin_class.admin_site))
    elif request.user.groups.filter(name='Class Tutor').exists():
        inline_instances.append(StudentInline(admin_class.model, admin_class.admin_site))
        # inline_instances.append(BatchInline(admin_class.model, admin_class.admin_site))
    return inline_instances

from django.contrib import admin
from django.contrib.auth import get_user_model

# def conditional_admin_registration(user):
#     # Get the admin site instance
#     admin_site = admin.site
#
#     # Unregister CustomUser if it's registered
#     if 'CustomUser' in admin_site._registry:
#         admin_site.unregister(get_user_model())
#
#     # Register Faculty if the user is in the 'College Admin' group
#     if user.groups.filter(name='College Admin').exists():
#         from .models import Faculty
#         from .admin import FacultyAdmin
#         admin_site.register(Faculty, FacultyAdmin)