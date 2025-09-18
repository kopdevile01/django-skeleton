"""Database models for hotel."""

from django.db import models


class Room(models.Model):
    # текстовое описание номера
    description = models.TextField()
    # цена за ночь с точностью до копеек
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # когда номер добавили
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # индексы: ускорят сортировку/фильтрацию
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:  # удобно видеть в админке/логах
        return f"Room(id={self.id}, price={self.price})"


class Booking(models.Model):
    # ссылка на номер; при удалении номера — удаляются и его брони
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    # даты брони (валидацию формата сделаем на уровне сериализаторов)
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # сортировать списки броней по дате начала
        ordering = ["date_start"]
        # индексы: быстрый доступ к броням конкретного номера по началу периода
        indexes = [
            models.Index(fields=["room", "date_start"]),
        ]

    def __str__(self) -> str:
        return f"Booking(id={self.id}, room_id={self.room_id}, {self.date_start}..{self.date_end})"
