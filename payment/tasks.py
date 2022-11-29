import sys

from django.db.models import Sum
from django.db.models.functions import Trunc
from payment.models import WeeklySalary, DailyIncome
from courier.models import Courier
from celery.utils.log import get_task_logger
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

logger = get_task_logger(__name__)

import datetime

def first_day_of_week(date):
    '''
    returns first day of week (Saturday) from given date
    '''
    td = (date.weekday() + 2) % 7
    first_day_of_week = date + datetime.timedelta(days = -td)
    return first_day_of_week


@shared_task
def update_weekly_salary() -> None:
    last_week_date = WeeklySalary.objects.all().order_by('-date_of_week')
    
    if last_week_date.exists():
        last_week_date = last_week_date[0].date_of_week + datetime.timedelta(days=+7)
    else:
        qs = DailyIncome.objects.all()
        if not qs.exists():
            logger.exception('{} - No entry in daily incomes, cannot update '\
                'weekly salary out of nothing.'.format(datetime.datetime.now()))
            return
        last_week_date = qs.order_by('date')[0].date

    last_updated_date = first_day_of_week(last_week_date)
    today = datetime.date.today()

    couriers = Courier.objects.all()
    for courier in couriers:
        start_of_week = last_updated_date
        while start_of_week < today:
            print(courier.daily_income.filter(
                date__gte=start_of_week, date__lte=start_of_week + datetime.timedelta(days=6)))
            qs = courier.daily_income.filter(
                date__gte=start_of_week, date__lte=start_of_week + datetime.timedelta(days=6)).aggregate(Sum('amount'))
            if qs['amount__sum'] is not None:
                try:
                    WeeklySalary.objects.create(
                        courier=courier, date_of_week=start_of_week, salary=qs['amount__sum'])
                    print('saved!')
                except:
                    logger.exception(sys.exc_info()[1])

            start_of_week += datetime.timedelta(7)
