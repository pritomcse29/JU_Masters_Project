from django.db import models


class Stop(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class RouteStop(models.Model):
    route = models.ForeignKey(Route, related_name='route_stops', on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    offset_minutes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('route', 'order')


class Bus(models.Model):
    name = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=30, unique=True)
    total_seats = models.PositiveIntegerField(default=40)

    def __str__(self):
        return f'{self.name} ({self.plate_number})'


class Schedule(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    fare = models.DecimalField(max_digits=8, decimal_places=2)