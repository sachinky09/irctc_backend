from django.db import models

class Train(models.Model):
    train_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=110)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.train_number} - {self.name}"