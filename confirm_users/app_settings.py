from django.conf import settings

USER_EDIT_FORM = getattr(settings, "USER_EDIT_FORM", "confirm_users.apps.user.UserForm")
