from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsPassengerRole
from transport.models import Schedule
from .models import Booking
from .serializers import BookingSerializer


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsPassengerRole]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError('Seat already booked')


class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')


class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'cancelled'})


class SeatListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, schedule_id):
        schedule = get_object_or_404(Schedule, pk=schedule_id)
        taken = set(
            Booking.objects.filter(schedule=schedule)
            .exclude(status='cancelled')
            .values_list('seat_number', flat=True)
        )
        seats = [{'seat': n, 'booked': n in taken} for n in range(1, schedule.bus.total_seats + 1)]
        return Response(seats)