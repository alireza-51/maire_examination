import sys
from django.utils.translation import gettext_lazy as _
from django.db import models

from courier.models import Courier



class Income(models.Model):
    courier = models.ForeignKey(Courier, null=False, blank=False, on_delete=models.CASCADE, related_name='income')
    date = models.DateField()
    amount = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True) # Describe where is this income coming from or why if it's decreasing income

    def __str__(self) -> str:
        return '{} {}'.format(self.courier, self.amount)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        try:
            daily_income = DailyIncome.objects.get(courier=self.courier, date=self.date)
            daily_income.amount += self.amount
            daily_income.save()
        except DailyIncome.DoesNotExist:
            daily_income = DailyIncome.objects.create(courier=self.courier, amount=self.amount, date=self.date)
        except:
            self.delete()
            raise sys.exc_info()[0](sys.exc_info()[1])



class DailyIncome(models.Model):
    courier = models.ForeignKey(Courier, null=False, blank=False, on_delete=models.CASCADE, related_name='daily_income')
    date = models.DateField()
    amount = models.IntegerField(null=False, blank=False)

    def __str__(self) -> str:
        return '{} {}'.format(self.courier, self.amount)


class WeeklySalary(models.Model):
    courier = models.ForeignKey(Courier, null=False, blank=False, on_delete=models.CASCADE, related_name='salary')
    date_of_week = models.DateField(null=False, blank=False)
    salary = models.IntegerField(default=0)
