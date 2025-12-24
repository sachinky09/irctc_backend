from django.db import models
from users.models import User
from trains.models import Train

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="bookings")
    seats_booked = models.PositiveIntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.email} - {self.train.train_number}"
