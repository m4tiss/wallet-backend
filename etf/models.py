from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserEtf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_etfs')
    name = models.CharField(max_length=100)
    purchase_date = models.DateField(auto_now_add=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f"{self.name} ({self.units} units @ {self.purchase_price})"

    @property
    def total_invested(self):
        return self.purchase_price * self.units
