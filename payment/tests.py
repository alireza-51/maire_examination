from datetime import date, timedelta

from django.test import TestCase
from .models import Income, DailyIncome, WeeklySalary
from courier.models import Courier

from payment.celery import update_weekly_salary


def today() -> date:
    return date(year=2022, month=11, day=28)

class IncomeTest(TestCase):
    def setUp(self) -> None:
        self.courier = Courier.objects.create(first_name='test', last_name='test')
        return super().setUp()

    def test_income_dailyincome_consistency(self):
        income = Income.objects.create(courier=self.courier, date=today(), amount=500)
        daily_income = DailyIncome.objects.get(courier=self.courier, date=today())
        self.assertEqual(daily_income.amount, 500)
        self.assertEqual(income.date, daily_income.date)
        income.delete() # in case of execution in order
        daily_income.delete() # in case of execution in order

    def test_daily_income_addition(self):
        Income.objects.create(courier=self.courier, date=today(), amount=500)
        Income.objects.create(courier=self.courier, date=today(), amount=700)
        Income.objects.create(courier=self.courier, date=today(), amount=-200)
        yesterday_income = Income.objects.create(courier=self.courier, date=today() - timedelta(days=1), amount=500)
        daily_income = DailyIncome.objects.get(courier=self.courier, date=today())
        self.assertEqual(daily_income.amount, 1000)


class SalaryTest(TestCase):
    def setUp(self) -> None:
        self.courier1 = Courier.objects.create(first_name='test1', last_name='test1')
        self.courier2 = Courier.objects.create(first_name='test2', last_name='test2')
        self.income1 = Income.objects.create(courier=self.courier1, amount=1000, date=today())
        self.income2 = Income.objects.create(courier=self.courier2, amount=500, date=today())
        return super().setUp()

    def weekly_salary_summation(self):
        '''
        Tests calculation of aggregation.
        '''
        income1_2 = Income.objects.create(courier=self.courier1, amount=500, date=today()+timedelta(days=1))
        income2_2 = Income.objects.create(courier=self.courier2, amount=500, date=today()+timedelta(days=1))
        update_weekly_salary()
        courier1_salary = WeeklySalary.objects.filter(courier=self.courier1)
        courier2_salary = WeeklySalary.objects.filter(courier=self.courier2)
        self.assertEqual(len(courier1_salary), 1)
        self.assertEqual(len(courier2_salary), 1)
        self.assertEqual(courier1_salary[0].salary, 1500)
        self.assertEqual(courier2_salary[0].salary, 1000)
    
    def weekly_salary_weeks(self):
        '''
        Tests days of week for calculation.
        '''
        income1_2 = Income.objects.create(courier=self.courier1, amount=500, date=today()+timedelta(days=8))
        income2_2 = Income.objects.create(courier=self.courier2, amount=500, date=today()+timedelta(days=8))
        income1_3 = Income.objects.create(courier=self.courier1, amount=500, date=today()+timedelta(days=16))
        income2_3 = Income.objects.create(courier=self.courier2, amount=500, date=today()+timedelta(days=16))
        update_weekly_salary()
        courier1_salary = WeeklySalary.objects.filter(courier=self.courier1)
        courier2_salary = WeeklySalary.objects.filter(courier=self.courier2)
        self.assertEqual(courier1_salary[0].salary, 1500)
        self.assertEqual(courier1_salary[1].salary, 500)
        self.assertEqual(courier1_salary[2].salary, 500)
        
        self.assertEqual(courier2_salary[0].salary, 1000)
        self.assertEqual(courier2_salary[1].salary, 500)
        self.assertEqual(courier2_salary[2].salary, 500)

    def test_orderly(self):
        '''
        Because of calcultaions it is important to run in specific order.
        '''
        self.weekly_salary_summation()
        self.weekly_salary_weeks()
