from django.apps import AppConfig


class CodesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'codes'
    verbose_name = 'Коды'

    def ready(self):
        import codes.signals
