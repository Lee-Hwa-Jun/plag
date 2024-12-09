from django.apps import AppConfig

class DrawConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'draw'

    def ready(self):
        from draw.scheduler import start_scheduler
        start_scheduler()