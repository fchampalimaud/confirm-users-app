from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from notifications.tools import notify

# set a new user inactive by default
@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance.pk is None and not instance.is_superuser:
        instance.is_active = False


        for user in User.objects.filter(is_superuser=True):

            notify(
                'USER_WAITING_APPROVAL',
                f'The new user {instance.username} requires your approval for access',
                f'The new user {instance.username} with the email {instance.email}, requires your approval for access.',
                user=user
            )