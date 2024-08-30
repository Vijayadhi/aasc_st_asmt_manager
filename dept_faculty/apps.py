from django.apps import AppConfig


class DeptFacultyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dept_faculty'
    verbose_name = 'Faculty Section'

    def ready(self):
        import dept_faculty.signals
