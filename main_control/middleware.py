# from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.utils.deprecation import MiddlewareMixin
#
#
# class AdminModelMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.user.is_authenticated:
#             # Unregister CustomUser if it is registered
#             if get_user_model() in admin.site._registry:
#                 admin.site.unregister(get_user_model())
#
#             # Conditionally register Fa   culty model
#             if request.user.groups.filter(name='College Admin').exists():
#                 from clg_admin.models import Faculty, FacultyAdmin
#                 # from .admin import
#                 if Faculty not in admin.site._registry:
#                     admin.site.register(Faculty, FacultyAdmin)
