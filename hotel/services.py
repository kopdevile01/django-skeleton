"""Business-logic (service layer) for the hotel app."""

from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Literal, Union

from django.db import transaction

from .models import Booking, Room


def create_room(description: str, price: Union[str, Decimal]) -> int:
    """Создаёт номер и возвращает его id."""
    try:
        amount = Decimal(price)
    except (InvalidOperation, TypeError):
        raise ValueError("price must be a number")
    if amount <= 0:
        raise ValueError("price must be positive")
    with transaction.atomic():
        room = Room.objects.create(description=description, price=amount)
    return int(room.id)


def list_rooms(
    order_by: Literal["price", "created_at"] | str = "created_at",
    order: Literal["asc", "desc"] | str = "asc",
) -> list[dict]:
    """Список номеров с сортировкой по цене/дате добавления."""
    allowed_fields = {"price", "created_at"}
    field = order_by if order_by in allowed_fields else "created_at"
    direction = "" if order == "asc" else "-"
    qs = (
        Room.objects.all()
        .order_by(f"{direction}{field}")
        .values("id", "description", "price", "created_at")
    )
    return list(qs)


def delete_room(room_id: int) -> bool:
    """Удаляет номер (и каскадно его брони). Возвращает True, если что-то удалили."""
    deleted, _ = Room.objects.filter(pk=room_id).delete()
    return deleted > 0


def create_booking(room_id: int, date_start: date, date_end: date) -> int:
    """
    Создаёт бронь и возвращает её id.
    - room_id: существующий номер (проверяем наличия)
    - date_*: объекты date (DRF сериализатор превратит строки в date)
    """
    if date_end < date_start:
        raise ValueError("date_end must be on or after date_start")

    if not Room.objects.filter(pk=room_id).exists():
        raise ValueError("room_not_found")

    has_overlap = Booking.objects.filter(
        room_id=room_id,
        date_start__lt=date_end,
        date_end__gt=date_start,
    ).exists()
    if has_overlap:
        raise ValueError("room_unavailable")

    with transaction.atomic():
        b = Booking.objects.create(
            room_id=room_id,
            date_start=date_start,
            date_end=date_end,
        )
    return int(b.id)


def list_bookings(room_id: int) -> list[dict]:
    """Список броней номера, сортировка по date_start ASC."""
    return list(
        Booking.objects.filter(room_id=room_id)
        .order_by("date_start")
        .values("id", "date_start", "date_end")
    )


def delete_booking(booking_id: int) -> bool:
    """Удаляет бронь. True — если что-то удалили."""
    deleted, _ = Booking.objects.filter(pk=booking_id).delete()
    return deleted > 0
