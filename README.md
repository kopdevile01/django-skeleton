# django-skeleton — Hotel & Bookings API

Мини-сервис на **Django + DRF** для управления номерами отеля и бронированиями.

## Стек
- Python 3.12
- Django 5
- Django REST Framework
- PostgreSQL (в Docker), локально можно SQLite
- Poetry, Ruff, pre-commit
- Pytest + pytest-django

## Быстрый старт (Docker)
```bash
docker compose up -d --build
# сервер поднимется на http://127.0.0.1:8000
