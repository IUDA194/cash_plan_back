from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from users.models import User, Currency

class Operation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

