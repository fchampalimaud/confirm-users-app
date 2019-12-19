from django.core import mail
from django.contrib.auth import get_user_model
from django.test import override_settings, RequestFactory, TestCase
from django.urls import reverse

from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account.signals import email_confirmed

# required to load and connect signals
from confirm_users import signals  # noqa


User = get_user_model()


@override_settings(ROOT_URLCONF="allauth.urls")
class SignalTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.admin = self._create_user_with_signup_view(
            username="admin", is_superuser=True
        )

    def _create_user_with_signup_view(
        self, username, email_verified=True, is_active=False, is_superuser=False
    ):
        """Sign up a test user via allauth and returns it."""
        response = self.client.post(
            reverse("account_signup"),
            {
                "username": username,
                "email": username + "@test.com",
                "password1": "password",
                "password2": "password",
            },
        )

        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username=username)
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.is_staff = is_superuser
        user.save()

        email = EmailAddress.objects.get(user=user)
        email.verified = email_verified
        email.save()

        self.client.logout()
        mail.outbox = []

        return user

    def test_superusers_not_notified_on_new_user_account_creation(self):
        self._create_user_with_signup_view(username="new_user")
        self.assertEqual(len(mail.outbox), 0, "Inbox is not empty")

    def test_superusers_notified_on_new_user_email_confirmation(self):
        user = self._create_user_with_signup_view(username="user")
        email_address = EmailAddress.objects.get(user=user)

        email_confirmed.send(sender=EmailConfirmationHMAC, email_address=email_address)

        self.assertGreater(len(mail.outbox), 0, "Inbox is empty")

        self.assertIn(
            "account awaiting approval",
            mail.outbox[0].subject,
            "New account email not sent",
        )

    def test_user_notified_on_account_activation(self):
        user = self._create_user_with_signup_view(username="user")

        self.assertFalse(user.is_active)
        user.is_active = True
        user.save()
        self.assertEqual(len(mail.outbox), 1, "Inbox is empty")
        self.assertIn(
            "Access Granted",
            mail.outbox[0].subject,
            "Account activation email not sent",
        )
        self.assertTrue(user.is_active)

    def test_user_notified_on_account_removal(self):
        user = self._create_user_with_signup_view(username="user", is_active=True)

        self.assertTrue(user.is_active)
        user.delete()
        self.assertEqual(len(mail.outbox), 1, "Inbox is empty")
        self.assertIn(
            "Access Revoked", mail.outbox[0].subject, "Account removal email not sent",
        )
        self.assertTrue(user.is_active)
