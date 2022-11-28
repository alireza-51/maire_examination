import sys

from django.db.models import Sum
from django.db.models.functions import Trunc
from payment.models import WeeklySalary, DailyIncome
from courier.models import Courier
from celery.utils.log import get_task_logger
from celery import shared_task

logger = get_task_logger(__name__)

import datetime

# def first_day_of_week(date):
#     '''
#     returns first day of week (Saturday) from given date
#     '''
#     td = (date.weekday() + 2) % 7
#     first_day_of_week = date + datetime.timedelta(days = -td)
#     if date == first_day_of_week:
#         return first_day_of_week
#     else:
#         return first_day_of_week + datetime.timedelta(days=7)

@shared_task
def update_weekly_salary() -> None:
    last_week_date = WeeklySalary.objects.all().order_by('-date_of_week')
    
    if last_week_date.exists():
        last_week_date = last_week_date[0].date_of_week + datetime.timedelta(days=7)
    else:
        last_week_date= DailyIncome.objects.all().order_by('date')[0].date

    couriers = Courier.objects.all()
    for courier in couriers:
        query_set = courier.daily_income.filter(date__gte=last_week_date).annotate(
            week=Trunc('date', 'week')).values('week').annotate(salary=Sum('amount'))
        for week in query_set:
            try:
                WeeklySalary.objects.create(courier=courier, date_of_week=week['week'], salary=week['salary'])
            except:
                logger.exception(sys.exc_info()[1])