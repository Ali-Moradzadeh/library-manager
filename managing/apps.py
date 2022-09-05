from django.apps import AppConfig

class ManagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'managing'
    def ready(self) :
        from . import signals
