from rest_framework import serializers
from .models import Booking
from trains.models import Train

class BookingSerializer(serializers.ModelSerializer):
    train_number = serializers.CharField(source="train.train_number", read_only=True)
    train_name = serializers.CharField(source="train.name", read_only=True)
    source = serializers.CharField(source="train.source", read_only=True)
    destination = serializers.CharField(source="train.destination", read_only=True)
    departure_time = serializers.DateTimeField(source="train.departure_time", read_only=True)
    arrival_time = serializers.DateTimeField(source="train.arrival_time", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "train",
            "seats_booked",
            "booking_time",
            "train_number",
            "train_name",
            "source",
            "destination",
            "departure_time",
            "arrival_time"
        ]
        read_only_fields = ["user", "booking_time"]
