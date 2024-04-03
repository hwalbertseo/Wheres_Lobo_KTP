from typing import Any
from django.db import models

class Lobo(models.Model):
    location = models.CharField(max_length=255)
    time_seen = models.DateTimeField()
    is_claimed = models.BooleanField(default = False)
    claimed_by = models.CharField(max_length=255)
    claim_time = models.DateTimeField()
    
    def __str__(self):
        return f"location: {self.location} at {self.time_seen}. \n Claimed?: {self.is_claimed} by {self.claimed_by} at {self.claim_time}"
    