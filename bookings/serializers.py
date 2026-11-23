from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'schedule', 'seat_number', 'boarding_stop', 'dropping_stop', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

    def validate(self, data):
        schedule = data['schedule']
        seat = data['seat_number']

        if seat < 1 or seat > schedule.bus.total_seats:
            raise serializers.ValidationError('Invalid seat number')

        orders = {rs.stop_id: rs.order for rs in schedule.route.route_stops.all()}
        b = orders.get(data['boarding_stop'].id)
        d = orders.get(data['dropping_stop'].id)
        if b is None or d is None:
            raise serializers.ValidationError('Stop is not on this route')
        if b >= d:
            raise serializers.ValidationError('Boarding must be before dropping')

        taken = Booking.objects.filter(schedule=schedule, seat_number=seat).exclude(status='cancelled')
        if taken.exists():
            raise serializers.ValidationError('Seat already booked')
        return data