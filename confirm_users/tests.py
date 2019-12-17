
from django.core import mail

import pytest

def test_send_mail():
    # Use Django send_mail function to construct a message
    # Note that you don't have to use this function at all.
    # Any other way of sending an email in Django would work just fine.
    mail.send_mail(
         'Example subject here',
         'Here is the message body.',
         'from@example.com',
         ['to@example.com']
    )

    # Now you can test delivery and email contents
    assert len(mail.outbox) == 1, "Inbox is not empty"
    assert mail.outbox[0].subject == 'Subject here'
    assert mail.outbox[0].body == 'Here is the message.'
    assert mail.outbox[0].from_email == 'from@example.com'
    assert mail.outbox[0].to == ['to@example.com']
