from django.urls import path
from .views import BookingCreateView, MyBookingsView, CancelBookingView, SeatListView

urlpatterns = [
    path('', BookingCreateView.as_view()),
    path('my/', MyBookingsView.as_view()),
    path('<int:pk>/cancel/', CancelBookingView.as_view()),
    path('seats/<int:schedule_id>/', SeatListView.as_view()),
]