from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RoomCreateSerializer
from .services import create_room


@api_view(["POST"])
def create_room_view(request):
    """Создаёт номер отеля и возвращает {"room_id": <int>}."""
    ser = RoomCreateSerializer(data=request.data)
    if not ser.is_valid():
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    room_id = create_room(**ser.validated_data)
    return Response({"room_id": room_id}, status=status.HTTP_201_CREATED)
