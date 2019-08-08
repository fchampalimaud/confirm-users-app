from confapp import conf
from django.contrib.auth import get_user_model
from pyforms_web.widgets.django import ModelFormWidget

User = get_user_model()


class UserForm(ModelFormWidget):
    MODEL = User
    TITLE = "Edit User"
    LAYOUT_POSITION = conf.ORQUESTRA_NEW_TAB

    @property
    def title(self):
        try:
            return str(self.model_object)
        except AttributeError:
            pass  # apparently it defaults to App TITLE

    def get_visible_fields_names(self):
        ret = super().get_visible_fields_names()
        ret.remove("password")
        return ret
