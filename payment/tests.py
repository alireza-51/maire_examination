from datetime import date, timedelta

from django.test import TestCase
from .models import Income, DailyIncome
from courier.models import Courier

class IncomeTest(TestCase):
    def setUp(self) -> None:
        self.courier = Courier.objects.create(first_name='test', last_name='test')
        return super().setUp()

    def test_income_dailyincome_consistency(self):
        income = Income.objects.create(courier=self.courier, date=date.today(), amount=500)
        daily_income = DailyIncome.objects.get(courier=self.courier, date=date.today())
        self.assertEqual(daily_income.amount, 500)
        self.assertEqual(income.date, daily_income.date)
        income.delete() # in case of execution in order
        daily_income.delete() # in case of execution in order

    def test_daily_income_addition(self):
        Income.objects.create(courier=self.courier, date=date.today(), amount=500)
        Income.objects.create(courier=self.courier, date=date.today(), amount=700)
        Income.objects.create(courier=self.courier, date=date.today(), amount=-200)
        yesterday_income = Income.objects.create(courier=self.courier, date=date.today() - timedelta(days=1), amount=500)
        daily_income = DailyIncome.objects.get(courier=self.courier, date=date.today())
        self.assertEqual(daily_income.amount, 1000)
