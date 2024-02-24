from django.apps import AppConfig
#import redis


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "simpleapp"

    def ready(self):
        import simpleapp.signals
