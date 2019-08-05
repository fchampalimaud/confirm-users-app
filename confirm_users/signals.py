from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from allauth.account.signals import email_confirmation_sent
from allauth.socialaccount.models import SocialAccount

from notifications.tools import notify


User = get_user_model()


if not hasattr(settings, 'ACCOUNT_EMAIL_VERIFICATION') or settings.ACCOUNT_EMAIL_VERIFICATION!='mandatory':


    # set a new user inactive by default
    @receiver(pre_save, sender=User)
    def set_new_user_inactive(sender, instance, **kwargs):
        if instance.pk is None and not instance.is_superuser:
            instance.is_active = False

            for u in User.objects.filter(is_superuser=True):

                notify(
                    'USER_WAITING_APPROVAL',
                    f'The new user {instance.username} requires your approval for access',
                    f'The new user {instance.username} with the email {instance.email}, requires your approval for access.',
                    user=u
                )


else:

    def set_new_user_inactive_account(request, confirmation, signup, **kwargs):
        email_address = confirmation.email_address
        instance = email_address.user

        if email_address.verified==False and not instance.is_superuser:
            instance.is_active = False
            instance.save()

            for u in User.objects.filter(is_superuser=True):

                notify(
                    'USER_WAITING_APPROVAL',
                    f'The new user {instance.username} requires your approval for access',
                    f'The new user {instance.username} with the email {instance.email}, requires your approval for access.',
                    user=u
                )

    email_confirmation_sent.connect(set_new_user_inactive_account)

    @receiver(pre_save, sender=SocialAccount)
    def set_new_user_inactive_socialaccount(sender, instance, **kwargs):

        if instance.pk is None:
            user = instance.user
            user.is_active = False
            user.save()

            for u in User.objects.filter(is_superuser=True):

                notify(
                    'USER_WAITING_APPROVAL',
                    f'The new user {user.username} requires your approval for access',
                    f'The new user {user.username} with the email {user.email}, requires your approval for access.',
                    user=u
                )

