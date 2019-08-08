from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver

from allauth.account.models import EmailAddress
from allauth.account.models import EmailConfirmationHMAC
from allauth.account.signals import user_signed_up
from allauth.account.signals import email_confirmed

from notifications.tools import notify


User = get_user_model()


@receiver(user_signed_up, sender=User)
@receiver(email_confirmed, sender=EmailConfirmationHMAC)
def notify_superusers_of_new_account(sender, **kwargs):
    """Sends an email to all superusers alerting for a new account
    awaiting approval.
    """

    if sender == User:
        user = kwargs["user"]
    else:
        user = kwargs["email_address"].user

    primary_email = EmailAddress.objects.get_primary(user=user)

    if not user.is_active and primary_email.verified:
        for su in User.objects.filter(is_superuser=True):
            notify(
                "NEW_USER_WAITING_APPROVAL",
                f"New account awaiting approval",
                f"An account assotiated with the email {user.email} was created and requires your approval to access the database.",
                user=su,
            )


@receiver(pre_save, sender=User)
def notify_user_activated(sender, instance, **kwargs):
    """Notifies a user whose account has been activated."""

    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass  # do nothing on user creation
    else:
        if instance.is_active and obj.is_active != instance.is_active:
            email = EmailAddress.objects.get_primary(user=instance)
            if email is not None and email.verified:
                notify(
                    code="USER_APPROVED",
                    title="Access Granted",
                    text=f"The account associated with the e-mail {instance.email} was approved. You may now access the database.",
                    user=instance,
                )


@receiver(pre_delete, sender=User)
def notify_user_removed(sender, instance, **kwargs):
    """Notifies a user whose account has been removed."""

    email = EmailAddress.objects.get_primary(user=instance)
    if email is not None and email.verified:
        notify(
            code="USER_REMOVED",
            title="Access revoked",
            text=f"The account associated with the e-mail {instance.email} was removed.",
            user=instance,
        )
