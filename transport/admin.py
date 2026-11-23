from django.contrib import admin
from .models import Stop, Route, RouteStop, Bus, Schedule


class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1


class RouteAdmin(admin.ModelAdmin):
    inlines = [RouteStopInline]


admin.site.register(Stop)
admin.site.register(Route, RouteAdmin)
admin.site.register(Bus)
admin.site.register(Schedule)