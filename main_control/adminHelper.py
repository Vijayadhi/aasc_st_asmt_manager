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
        )

    else:
        # Default fieldsets for other users
        return super_func(request, obj)



def get_inline_instances_for_user(admin_class, request, obj=None):
    inline_instances = []
    if request.user.groups.filter(name='College Admin').exists():
        inline_instances.append(FacultyInline(admin_class.model, admin_class.admin_site))
    elif request.user.groups.filter(name='Class Tutor').exists():
        inline_instances.append(StudentInline(admin_class.model, admin_class.admin_site))
        # inline_instances.append(BatchInline(admin_class.model, admin_class.admin_site))
    return inline_instances
