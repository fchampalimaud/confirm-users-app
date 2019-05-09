from django.apps import AppConfig

class ConfirmUsersConfig(AppConfig):
    name = 'confirm_users'
    verbose_name = 'Confirm users'

    def ready(self):
        import confirm_users.signals