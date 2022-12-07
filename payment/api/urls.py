from django.urls import path
from .views import WeeklySalaryView, CalculateSalary

urlpatterns = [
    path('salary/', WeeklySalaryView.as_view({'get':'list'})),
    path('update/', CalculateSalary.as_view({'get':'list'}))
]