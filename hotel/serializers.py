from rest_framework import serializers


class RoomCreateSerializer(serializers.Serializer):
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
