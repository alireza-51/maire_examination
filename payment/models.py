from django.utils.translation import gettext_lazy as _
from django.db import models

from courier.models import Courier



class Income(models.Model):
    courier = models.ForeignKey(Courier, null=False, blank=False, on_delete=models.CASCADE, related_name='income')
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True) # Describe where is this income coming from or why if it's decreasing income

    def save(self, *args, **kwargs) -> None:
        daily_income = DailyIncome.objects.get(courier=self.courier, date=self.date)
        daily_income.amount += self.amount
        daily_income.save()
        return super().save(*args, **kwargs)

class DailyIncome(models.Model):
    courier = models.ForeignKey(Courier, null=False, blank=False, on_delete=models.CASCADE, related_name='daily_income')
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(null=False, blank=False)
