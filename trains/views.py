from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Train
from .serializers import TrainSerializer
from irctc_backend.mongo import mongo_collection
from datetime import datetime
import time


class TrainSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_time = time.time()

        source = request.GET.get("source")
        destination = request.GET.get("destination")
        date = request.GET.get("date")  # optional
        limit = request.GET.get("limit", 10)
        offset = request.GET.get("offset", 0)

        # Required params check (assignment strict)
        if not source or not destination:
            return Response(
                {"error": "source and destination are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Base query
        queryset = Train.objects.filter(
            source__iexact=source,
            destination__iexact=destination
        )

        # Optional date filter (YYYY-MM-DD)
        if date:
            try:
                parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
                queryset = queryset.filter(departure_time__date=parsed_date)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Pagination
        try:
            limit = int(limit)
            offset = int(offset)
        except ValueError:
            return Response(
                {"error": "limit and offset must be integers"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_count = queryset.count()
        trains = queryset[offset: offset + limit]

        serializer = TrainSerializer(trains, many=True)

        execution_time = round(time.time() - start_time, 4)

        # MongoDB logging (assignment requirement)
        mongo_collection.insert_one({
            "endpoint": "/api/trains/search/",
            "params": request.GET.dict(),
            "user_id": request.user.id,
            "execution_time": execution_time
        })

        return Response({
            "count": total_count,
            "results": serializer.data
        }, status=status.HTTP_200_OK)


class TrainCreateUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        train_number = request.data.get("train_number")

        if not train_number:
            return Response(
                {"error": "train_number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            train = Train.objects.get(train_number=train_number)
            serializer = TrainSerializer(train, data=request.data, partial=True)
        except Train.DoesNotExist:
            serializer = TrainSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
