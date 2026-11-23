from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase

from accounts.models import User
from transport.models import Stop, Route, RouteStop, Bus, Schedule
from bookings.models import Booking


class PaymentFlowTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='t1', email='t1@test.com', password='Test@12345'
        )
        self.client.force_authenticate(user=self.user)

        a = Stop.objects.create(name='A')
        b = Stop.objects.create(name='B')
        route = Route.objects.create(name='A to B')
        RouteStop.objects.create(route=route, stop=a, order=1, offset_minutes=0)
        RouteStop.objects.create(route=route, stop=b, order=2, offset_minutes=30)
        bus = Bus.objects.create(name='Bus', plate_number='X-1', total_seats=40)
        schedule = Schedule.objects.create(
            route=route, bus=bus,
            departure_time=timezone.now() + timedelta(days=1), fare=100,
        )
        self.booking = Booking.objects.create(
            user=self.user, schedule=schedule, seat_number=1,
            boarding_stop=a, dropping_stop=b,
        )

    def pay(self, outcome):
        return self.client.post(
            '/api/payments/pay/', {'booking': self.booking.id, 'outcome': outcome}
        )

    def test_failed_payment_keeps_pending(self):
        res = self.pay('failed')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['booking_status'], 'pending')

    def test_success_confirms_booking(self):
        res = self.pay('success')
        self.assertEqual(res.data['booking_status'], 'confirmed')

    def test_cannot_pay_twice(self):
        self.pay('success')
        res = self.pay('success')
        self.assertEqual(res.status_code, 400)

    def test_other_user_cannot_pay(self):
        other = User.objects.create_user(
            username='t2', email='t2@test.com', password='Test@12345'
        )
        self.client.force_authenticate(user=other)
        res = self.pay('success')
        self.assertEqual(res.status_code, 404)