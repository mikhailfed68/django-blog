from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Implicity connect signal handler 'post_save'
        # decorated with @receiver.
        from . import signals
