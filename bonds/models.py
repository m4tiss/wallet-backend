from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Bond(models.Model):
    TYPE_CHOICES = [
        ('standard', 'Standardowa'),
        ('family', 'Rodzinna'),
    ]

    INTEREST_TYPE_CHOICES = [
        ('fixed', 'Stałe'),
        ('variable', 'Zmienne'),
    ]

    name = models.CharField(max_length=100)
    duration_months = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='standard')

    interest_type = models.CharField(max_length=10, choices=INTEREST_TYPE_CHOICES)
    first_period_interest = models.DecimalField(max_digits=5, decimal_places=2, help_text="W skali roku, w %")
    margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                 help_text="Marża w %, jeśli dotyczy")

    def __str__(self):
        return self.name


class UserBond(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bonds')

    amount = models.PositiveIntegerField()
    purchase_date = models.DateField(auto_now_add=True)

    name = models.CharField(max_length=100)
    duration_months = models.PositiveIntegerField()

    BOND_TYPE_CHOICES = [
        ('standard', 'Standardowa'),
        ('family', 'Rodzinna'),
    ]
    INTEREST_TYPE_CHOICES = [
        ('fixed', 'Stałe'),
        ('variable', 'Zmienne'),
    ]

    type = models.CharField(max_length=10, choices=BOND_TYPE_CHOICES, default='standard')
    interest_type = models.CharField(max_length=10, choices=INTEREST_TYPE_CHOICES)
    first_period_interest = models.DecimalField(max_digits=5, decimal_places=2, help_text="W skali roku, w %")
    margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                 help_text="Marża w %, jeśli dotyczy")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.amount})"
