from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES =[
        ('passenger','Passenger'),
        ('admin','Admin'),
        ('operator','Operator'),
    ]
    email= models.EmailField(unique=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='passenger')


