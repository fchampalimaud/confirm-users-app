from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


# set a new user inactive by default
@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance.pk is None and not instance.is_superuser:
        instance.is_active = False
