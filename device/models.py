from django.db import models

# Create your models here.
class ESP32Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, default="LOLIN32")
    last_seen = models.DateTimeField(null=True, blank=True)
    led_state = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def is_online(self):
        if not self.last_seen:
            return False

        from django.utils import timezone
        from datetime import timedelta

        return timezone.now() - self.last_seen < timedelta(seconds=30)
