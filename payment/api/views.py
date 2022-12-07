from rest_framework import generics, viewsets, mixins
from django_filters import FilterSet,DateFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import WeeklySerializer
from payment.models import WeeklySalary
from payment.tasks import update_weekly_salary


class WeeklySalaryView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = WeeklySerializer
    # queryset = WeeklySalary.objects.all()

    def get_queryset(self):
        qs = WeeklySalary.objects.all()
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        if from_date:
            qs = qs.filter(date_of_week__gte=from_date)
        if to_date:
            qs = qs.filter(date_of_week__lte=to_date)
        return qs.select_related('courier')

class CalculateSalary(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = WeeklySerializer

    def get_queryset(self):
        update_weekly_salary()
        return WeeklySalary.objects.all().select_related('courier')
        