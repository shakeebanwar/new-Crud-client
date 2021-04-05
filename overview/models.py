from django.db import models
from django.utils import timezone
from users.models import Account
from organization.models import Organization, Office


class Booking(models.Model):
    LOCATION_OPTIONS = (
            ('H', 'Home Office'),
            ('O', 'Office'),
            ('N', 'Not indicated'),
    )
    account             = models.ForeignKey(Account, on_delete=models.CASCADE)
    organization        = models.ForeignKey(Organization, on_delete=models.CASCADE)
    office              = models.ForeignKey(Office, on_delete=models.CASCADE)
    booking_time        = models.DateTimeField(default=timezone.now)
    location            = models.CharField(max_length=100, choices=LOCATION_OPTIONS)
    class Meta:
            unique_together = ('account', 'booking_time',)
