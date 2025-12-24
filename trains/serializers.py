from rest_framework import serializers
from .models import Train

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = "__all__"

    def validate(self, data):
        total = data.get("total_seats")
        available = data.get("available_seats")

        if total is not None and available is not None:
            if available > total:
                raise serializers.ValidationError(
                    "available_seats cannot be greater than total_seats"
                )
        return data
