from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    priority = models.IntegerField()
    zone = models.CharField(max_length=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ticket {self.id}: Priority {self.priority}, Zone {self.zone}, Created by {self.created_by.username}"
