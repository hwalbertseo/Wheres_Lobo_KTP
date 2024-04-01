from typing import Any
from django.db import models

class Lobo(models.Model):
    location = models.CharField(max_length=255)
    time_seen = models.DateTimeField()
    is_claimed = models.CharField(max_length=10, default = False)
    claimed_by = models.CharField(max_length=255)
    claim_time = models.DateTimeField()
    
    def __str__(self):
        return f"location: {self.location} at {self.time_seen}. \n Claimed?: {self.is_claimed} by {self.claimed_by} at {self.claim_time}"
    
class User(models.Model):
    name = models.CharField(max_length=255)
    phone_Num = models.IntegerField(default = 0)
    email = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Name: {self.name} \n Email: {self.email}"