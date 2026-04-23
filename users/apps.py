from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    default_auto_field = 'django.db.models.BigAutoField'
    
    def ready(self):
        # Importar signals quando a app está pronta
        import users.models
