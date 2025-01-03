from django.apps import AppConfig


class GymtemploadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gymtemploadmin'

    def ready(self):
        import gymtemploadmin.signals
