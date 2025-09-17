"""Business-logic (service layer) for the hotel app."""

from decimal import Decimal, InvalidOperation
from typing import Union

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
