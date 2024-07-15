# main/apps.py

from django.apps import AppConfig

# Defining the configuration for the 'main' app
class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    # Import signals when the app is ready
    def ready(self):
        import main.signals
