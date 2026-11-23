from django.urls import path
from .views import DemoPayView

urlpatterns = [
    path('pay/', DemoPayView.as_view()),
]