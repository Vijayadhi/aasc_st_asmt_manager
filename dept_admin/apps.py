from django.apps import AppConfig


class DeptAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dept_admin'
    verbose_name = "HOD Actions"

    def ready(self):
        import dept_admin.signals