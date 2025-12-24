from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Booking
from .serializers import BookingSerializer
from trains.models import Train
from django.db import transaction

class BookingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        train_id = request.data.get("train")
        seats_to_book = request.data.get("seats_booked")

        if not train_id or not seats_to_book:
            return Response(
                {"error": "train and seats_booked are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            seats_to_book = int(seats_to_book)
            if seats_to_book <= 0:
                raise ValueError
        except ValueError:
            return Response(
                {"error": "seats_booked must be a positive integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            train = Train.objects.get(id=train_id)
        except Train.DoesNotExist:
            return Response({"error": "Train not found"}, status=status.HTTP_404_NOT_FOUND)

        if train.available_seats < seats_to_book:
            return Response({"error": "Not enough available seats"}, status=status.HTTP_400_BAD_REQUEST)

        # Use transaction to avoid race conditions
        with transaction.atomic():
            train.available_seats -= seats_to_book
            train.save()

            booking = Booking.objects.create(user=user, train=train, seats_booked=seats_to_book)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyBookingsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        bookings = Booking.objects.filter(user=user).select_related("train")
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
