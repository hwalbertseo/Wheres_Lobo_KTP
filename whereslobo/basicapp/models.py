from django.db import models

# Create your models here.
from django.db import models

class Lobo(models.Model):
    location = models.CharField(max_length=255)
    time_seen = models.CharField(max_length=10)
    is_claimed = models.CharField(max_length=10)
    claimed_by = models.CharField(max_length=255)

    def __str__(self):
        return f"location: {self.location} at {self.time_seen}. Claimed?: {self.is_claimed} by {self.claimed_by}"