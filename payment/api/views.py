from rest_framework import generics, viewsets, mixins
from django_filters import FilterSet,DateFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import WeeklySerializer
from payment.models import WeeklySalary


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
        return qs