import uuid
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsPassengerRole
from bookings.models import Booking
from .models import Payment


class DemoPayView(APIView):
    permission_classes = [IsPassengerRole]

    def post(self, request):
        booking = get_object_or_404(
            Booking, pk=request.data.get('booking'), user=request.user
        )
        outcome = request.data.get('outcome')

        if outcome not in ('success', 'failed', 'cancelled'):
            raise ValidationError('outcome must be success, failed or cancelled')
        if booking.status != 'pending':
            raise ValidationError('Booking is not pending')

        payment = Payment.objects.create(
            booking=booking,
            amount=booking.schedule.fare,
            status=outcome,
            reference=uuid.uuid4().hex,
        )

        if outcome == 'success':
            booking.status = 'confirmed'
            booking.save()
        elif outcome == 'cancelled':
            booking.status = 'cancelled'
            booking.save()

        return Response({
            'payment_status': payment.status,
            'booking_status': booking.status,
            'reference': payment.reference,
        })