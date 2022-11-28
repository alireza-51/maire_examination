from django.contrib import admin
from .models import Income, DailyIncome, WeeklySalary


class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'courier', 'date', 'amount']

class SalaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'courier', 'date_of_week', 'salary']

admin.site.register(Income, IncomeAdmin)
admin.site.register(DailyIncome, IncomeAdmin)
admin.site.register(WeeklySalary, SalaryAdmin)
