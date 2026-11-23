from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import Stop, Schedule


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ['id', 'name']


class ScheduleSerializer(serializers.ModelSerializer):
    route = serializers.CharField(source='route.name')
    bus = serializers.CharField(source='bus.name')
    stops = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['id', 'route', 'bus', 'departure_time', 'fare', 'stops']

    def get_stops(self, obj):
        start = timezone.localtime(obj.departure_time)
        result = []
        for rs in obj.route.route_stops.all():
            t = start + timedelta(minutes=rs.offset_minutes)
            result.append({'stop': rs.stop.name, 'time': t.strftime('%I:%M %p')})
        return result