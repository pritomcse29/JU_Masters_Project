from django.conf import settings
from django.db import models
from django.db.models import Q
from transport.models import Schedule, Stop


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookings', on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    boarding_stop = models.ForeignKey(Stop, related_name='+', on_delete=models.PROTECT)
    dropping_stop = models.ForeignKey(Stop, related_name='+', on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['schedule', 'seat_number'],
                condition=~Q(status='cancelled'),
                name='unique_active_seat',
            )
        ]