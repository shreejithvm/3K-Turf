from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date,time


# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # enforce uniqueness

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


SPORT_CHOICES = [
    ("Cricket", "Cricket"),
    ("Football", "Football"),
    ("Badminton", "Badminton"),
]

DISTRICT_CHOICES = [
    ("Kasaragod", "Kasaragod"),
    ("Kannur", "Kannur"),
    ("Kozhikode", "Kozhikode"),
]

class Turf(models.Model):
    name = models.CharField(max_length=150)
    sport = models.CharField(max_length=30, choices=SPORT_CHOICES)
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES)
    address = models.TextField(blank=True)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='turfs/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.sport} ({self.district})"



class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=date.today)
    start_time = models.TimeField(default=time(6, 0))
    end_time = models.TimeField(default=time(7, 0))

    def __str__(self):
        return f"{self.user.email} - {self.turf.name} on {self.date}"