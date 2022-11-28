from django.urls import path
from .views import WeeklySalaryView

urlpatterns = [
    path('salary/', WeeklySalaryView.as_view({'get':'list'})),
]