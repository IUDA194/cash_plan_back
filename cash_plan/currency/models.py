from django.db import models
from django.db.models.signals import post_migrate

from django.dispatch import receiver

class Currency(models.Model):
    name = models.CharField(max_length=228)
    full_name = models.CharField(max_length=456)
    
    def __str__(self) -> str:
        return f"{self.full_name}"

@receiver(post_migrate)
def create_default_currency(sender, **kwargs):
    if sender.name == 'currency':
        Currency = sender.get_model('Currency')
        if not Currency.objects.filter(name='USD').exists():
            Currency.objects.create(name='USD', full_name='United States Dollar')
        if not Currency.objects.filter(name='EUR').exists():
            Currency.objects.create(name='EUR', full_name='Euro')

