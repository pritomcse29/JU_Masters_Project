from django.urls import path
from .views import StopListView, ScheduleListView

urlpatterns = [
    path('stops/', StopListView.as_view()),
    path('schedules/', ScheduleListView.as_view()),
]