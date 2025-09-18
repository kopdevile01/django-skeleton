from decimal import Decimal

from rest_framework import serializers


class RoomCreateSerializer(serializers.Serializer):
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.01"))


class BookingCreateSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(min_value=1)
    date_start = serializers.DateField()
    date_end = serializers.DateField()

    def validate(self, attrs):
        if attrs["date_end"] < attrs["date_start"]:
            raise serializers.ValidationError({"date_end": "must be on or after date_start"})
        return attrs


class BookingListQuerySerializer(serializers.Serializer):
    room_id = serializers.IntegerField(min_value=1)


class BookingDeleteSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField(min_value=1)
