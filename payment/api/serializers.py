from rest_framework import serializers

from payment.models import WeeklySalary
from courier.models import Courier

class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class WeeklySerializer(serializers.ModelSerializer):
    courier = CourierSerializer()
    
    class Meta:
        model = WeeklySalary
        fields = '__all__'
        depth = 1

