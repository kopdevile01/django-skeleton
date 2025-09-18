import pytest

from hotel.models import Room


@pytest.mark.django_db
def test_bookings_create_conflict_returns_400(api):
    room = Room.objects.create(description="Economy", price="99.99")

    # базовая бронь
    base = {"room_id": room.id, "date_start": "2025-12-30", "date_end": "2026-01-02"}
    resp1 = api.post("/bookings/create/", base, format="json")
    assert resp1.status_code == 201, resp1.content

    # пересекающаяся бронь
    overlap = {"room_id": room.id, "date_start": "2025-12-31", "date_end": "2026-01-01"}
    resp2 = api.post("/bookings/create/", overlap, format="json")

    assert resp2.status_code == 400, resp2.content
    assert resp2.json() == {"detail": "room is not available for these dates"}
