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


def create_booking(room_id: int, date_start: str, date_end: str) -> int:
    """Создаёт бронь и возвращает её id.
    - room_id: ID существующего номера (FK не проверяем вручную — БД/ORM валидирует)
    - date_*: строки в формате YYYY-MM-DD
    - НЕ проверяем занятость (по заданию это опционально)
    """
    try:
        ds = date.fromisoformat(date_start)
        de = date.fromisoformat(date_end)
    except ValueError as e:
        raise ValueError("dates must be in YYYY-MM-DD format") from e
    if de < ds:
        raise ValueError("date_end must be on or after date_start")

    with transaction.atomic():
        b = Booking.objects.create(room_id=room_id, date_start=ds, date_end=de)
    return int(b.id)
