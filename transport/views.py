from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from .models import Stop, Schedule
from .serializers import StopSerializer, ScheduleSerializer


class StopListView(generics.ListAPIView):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Schedule.objects.select_related('route', 'bus')
        date = self.request.query_params.get('date')
        stop = self.request.query_params.get('stop')
        if date:
            qs = qs.filter(departure_time__date=date)
        if stop:
            qs = qs.filter(route__route_stops__stop__name__icontains=stop).distinct()
        return qs