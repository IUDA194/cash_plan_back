from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Currency(models.Model):
    name = models.CharField(max_length=228)
    full_name = models.CharField(max_length=456)

class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', unique=True, null=True, blank=True)
    password = models.CharField(max_length=258, verbose_name='password', null=True, blank=True)
    regestration_date = models.DateTimeField(verbose_name="Regestration date", default=timezone.now)
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE, null=True, blank=True, default=1)
    daily_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="custom_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_permissions",
        related_query_name="user_permission",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.email}"

@receiver(post_migrate)
def create_default_currency(sender, **kwargs):
    if sender.name == 'users':  # Замените 'your_app_name' на имя вашего приложения
        Currency = sender.get_model('Currency')
        if not Currency.objects.filter(name='USD').exists():
            Currency.objects.create(name='USD', full_name='United States Dollar')

