from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from clg_admin.models import Faculty
from main_control.adminHelper import get_fieldsets_for_user, get_inline_instances_for_user
from main_control.forms import CustomUserCreationForm, CustomUserChangeForm
from main_control.models import CustomUser



class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('name', 'email', 'faculty_type_display', 'is_current_user')
    list_filter = ('email', 'name',)
    list_display_links = ["email", 'name']
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        ("Basic Profile Details", {'fields': ('email', 'name')}),
        ("Personal Information", {'fields': ('blood_group', 'address', 'dob', 'mobile_no', 'groups')}),
        ("Permissions", {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        ("Basic Profile Details", {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile_no', 'groups'),
        }),
    )

    def faculty_type_display(self, obj):
        """
        Display the faculty_type from the related Faculty model.
        """
        faculty = Faculty.objects.filter(user=obj).first()

        if faculty:
            roles = faculty.faculty_type.all()  # Get all roles related to the faculty
            return ', '.join([role.name for role in roles]) if roles else 'Student'
        else:
            return 'Not Assigned'

    faculty_type_display.short_description = 'Faculty Type'

    def get_fieldsets(self, request, obj=None):
        return get_fieldsets_for_user(super().get_fieldsets, request, obj)

    def get_inline_instances(self, request, obj=None):
        # if obj is None:  # obj is None when creating a new object
        return get_inline_instances_for_user(self, request, obj)
        # return []  # Return an empty list when editing an existing object

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(')(aasc-mrk-gen)(')
            # obj.is_staff = True
            # obj.is_active = True
        super().save_model(request, obj, form, change)



    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        current_user = request.user

        # Create a queryset for the current user
        user_in_queryset = queryset.filter(id=current_user.id)

        # Initialize an empty queryset for the roles
        role_based_queryset = queryset.none()

        # Check for each role and combine the querysets
        if current_user.groups.filter(name='College Admin').exists():
            # Show users in the Faculty group
            faculty_group = Group.objects.get(name='Faculty')
            role_based_queryset = role_based_queryset | queryset.filter(groups=faculty_group)

        if current_user.groups.filter(name='FacultyAdmin').exists():
            # Show users in the Faculty group
            faculty_group = Group.objects.get(name='Faculty')
            role_based_queryset = role_based_queryset | queryset.filter(groups=faculty_group)

        if current_user.groups.filter(name='Class Tutor').exists():
            # Show users in the Student group
            student_group = Group.objects.get(name='Student')
            role_based_queryset = role_based_queryset | queryset.filter(groups=student_group)

        if current_user.groups.filter(name='Faculty').exists():
            # Show users in the Student group
            student_group = Group.objects.get(name='Student')
            role_based_queryset = role_based_queryset | queryset.filter(groups=student_group)

        # Ensure the current user is included only once and combine with role-based queryset
        final_queryset = (role_based_queryset | user_in_queryset).distinct()

        return final_queryset
    def is_current_user(self, obj):
        request = self._get_request()  # Retrieve the request object
        return obj.id == request.user.id

    is_current_user.short_description = 'Current User'
    is_current_user.boolean = True

    def _get_request(self):
        # This method is just a placeholder to indicate where the request comes from.
        # In practice, you pass the request directly where needed.
        import inspect
        frame = inspect.currentframe().f_back
        while frame:
            if 'request' in frame.f_locals:
                return frame.f_locals['request']
            frame = frame.f_back
        return None

   
    jazzmin_section_order = ("Basic Profile Details", "Personal Information", "Permissions")


admin.site.register(CustomUser, CustomUserAdmin)
