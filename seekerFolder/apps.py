from django.apps import AppConfig


class SeekerfolderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seekerFolder'

    def ready(self):
        from . import signals
