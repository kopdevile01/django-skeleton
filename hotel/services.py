"""Business-logic (service layer) for the hotel app."""

from decimal import Decimal, InvalidOperation
from typing import Literal, Union

from django.db import transaction

from .models import Room


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
