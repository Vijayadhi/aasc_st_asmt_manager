from django.apps import AppConfig


class ClgAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clg_admin'

    def ready(self):
        import clg_admin.signals
