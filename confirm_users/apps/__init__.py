from django.apps import AppConfig


class ConfirmUsersConfig(AppConfig):
    name = "confirm_users"
    verbose_name = "Confirm users"

    def ready(self):
        from .. import signals

        from .dashboard import Dashboard

        global Dashboard
