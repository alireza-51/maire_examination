from django.contrib import admin
from .models import Income, DailyIncome


class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'courier', 'date', 'amount']

admin.site.register(Income, IncomeAdmin)
admin.site.register(DailyIncome, IncomeAdmin)
