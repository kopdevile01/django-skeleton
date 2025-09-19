import pytest

from hotel.models import Booking, Room


@pytest.mark.django_db
def test_bookings_create_success(api):
    room = Room.objects.create(description="Economy", price="99.99")

    payload = {"room_id": room.id, "date_start": "2025-12-30", "date_end": "2026-01-02"}
    resp = api.post("/bookings/create/", payload, format="json")

    assert resp.status_code == 201, resp.content
    data = resp.json()
    assert "booking_id" in data

    b = Booking.objects.get(id=data["booking_id"])
    assert b.room_id == room.id
    assert str(b.date_start) == "2025-12-30"
    assert str(b.date_end) == "2026-01-02"
