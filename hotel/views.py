from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    BookingCreateSerializer,
    BookingDeleteSerializer,
    BookingListQuerySerializer,
    RoomCreateSerializer,
)
from .services import (
    create_booking,
    create_room,
    delete_booking,
    delete_room,
    list_bookings,
    list_rooms,
)


@extend_schema(
    methods=["POST"],
    tags=["rooms"],
    summary="Create room",
    description="Создаёт номер.",
    request=RoomCreateSerializer,
    responses={
        201: OpenApiResponse(OpenApiTypes.OBJECT, description='{"room_id": int}'),
        400: OpenApiResponse(description="validation error"),
    },
)
@extend_schema(
    methods=["GET"],
    tags=["rooms"],
    summary="List rooms",
    description="Список номеров.",
    parameters=[
        OpenApiParameter(name="order_by", required=False, type=str, enum=["price", "created_at"]),
        OpenApiParameter(name="order", required=False, type=str, enum=["asc", "desc"]),
    ],
    responses={200: OpenApiResponse(OpenApiTypes.OBJECT, description="[... rooms ...]")},
)
@api_view(["POST", "GET"])
def rooms_collection(request):
    """POST: создать номер → {"room_id": int}; GET: список номеров с сортировкой."""
    if request.method == "POST":
        ser = RoomCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        room_id = create_room(**ser.validated_data)
        return Response({"room_id": room_id}, status=status.HTTP_201_CREATED)

    order_by = request.query_params.get("order_by", "created_at")
    order = request.query_params.get("order", "asc")
    data = list_rooms(order_by=order_by, order=order)
    return Response(data, status=status.HTTP_200_OK)


@extend_schema(
    methods=["DELETE"],
    tags=["rooms"],
    summary="Delete room",
    description="Удаляет номер по ID.",
    responses={
        200: OpenApiResponse(OpenApiTypes.OBJECT, description='{"status":"ok"}'),
        404: OpenApiResponse(description="room not found"),
    },
)
@api_view(["DELETE"])
def rooms_item(request, room_id: int):
    """Удаляет номер отеля по ID: {"status": "ok"} или 404."""
    if delete_room(room_id):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    return Response({"detail": "room not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    methods=["POST"],
    tags=["bookings"],
    summary="Create booking",
    description="Создаёт бронь.",
    request=BookingCreateSerializer,
    responses={
        201: OpenApiResponse(OpenApiTypes.OBJECT, description='{"booking_id": int}'),
        400: OpenApiResponse(description="validation error / room_unavailable"),
        404: OpenApiResponse(description="room not found"),
    },
)
@api_view(["POST"])
def bookings_create(request):
    ser = BookingCreateSerializer(data=request.data)
    if not ser.is_valid():
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        booking_id = create_booking(**ser.validated_data)
    except ValueError as e:
        msg = str(e)
        if msg == "room_not_found":
            return Response({"detail": "room not found"}, status=status.HTTP_404_NOT_FOUND)
        if msg == "room_unavailable":
            return Response(
                {"detail": "room is not available for these dates"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"booking_id": booking_id}, status=status.HTTP_201_CREATED)


@extend_schema(
    methods=["GET"],
    tags=["bookings"],
    summary="List bookings",
    description="Список броней номера. Отсортировано по date_start.",
    parameters=[
        OpenApiParameter(
            name="room_id",
            type=int,  # или OpenApiTypes.INT
            location=OpenApiParameter.QUERY,
            required=True,
            description="ID номера",
        ),
    ],
    responses={
        200: OpenApiResponse(
            OpenApiTypes.OBJECT,
            description=(
                '[{"id": int, "date_start": "YYYY-MM-DD", "date_end": "YYYY-MM-DD"}, ...]'
            ),
        ),
        400: OpenApiResponse(description="validation error"),
    },
)
@api_view(["GET"])
def bookings_list(request):
    """Список броней номера: ?room_id=<int> → [{id, date_start, date_end}, ...]."""
    ser = BookingListQuerySerializer(data=request.query_params)
    if not ser.is_valid():
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    data = list_bookings(**ser.validated_data)
    return Response(data, status=status.HTTP_200_OK)


@extend_schema(
    methods=["POST"],
    tags=["bookings"],
    summary="Delete booking",
    description="Удаляет бронь по booking_id.",
    request=BookingDeleteSerializer,
    responses={
        200: OpenApiResponse(OpenApiTypes.OBJECT, description='{"status":"ok"}'),
        404: OpenApiResponse(description="booking not found"),
        400: OpenApiResponse(description="validation error"),
    },
)
@api_view(["POST"])
def bookings_delete(request):
    """Удалить бронь по ID: {"booking_id": int} → {"status":"ok"} или 404."""
    ser = BookingDeleteSerializer(data=request.data)
    if not ser.is_valid():
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    ok = delete_booking(**ser.validated_data)
    if ok:
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    return Response({"detail": "booking not found"}, status=status.HTTP_404_NOT_FOUND)
