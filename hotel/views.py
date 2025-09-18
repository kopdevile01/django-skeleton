from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RoomCreateSerializer
from .services import create_room, list_rooms


@api_view(["POST", "GET"])
def rooms_collection(request):
    """POST: создать номер → {"room_id": int}; GET: список номеров с сортировкой."""
    if request.method == "POST":
        ser = RoomCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        room_id = create_room(**ser.validated_data)
        return Response({"room_id": room_id}, status=status.HTTP_201_CREATED)

    # GET
    order_by = request.query_params.get("order_by", "created_at")
    order = request.query_params.get("order", "asc")
    data = list_rooms(order_by=order_by, order=order)
    return Response(data, status=status.HTTP_200_OK)
