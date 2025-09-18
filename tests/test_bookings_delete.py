from datetime import date

import pytest

from hotel.models import Booking, Room


@pytest.mark.django_db
def test_bookings_delete_ok_then_404(api):
    room = Room.objects.create(description="Del room", price="20.00")
    b = Booking.objects.create(room=room, date_start=date(2025, 2, 1), date_end=date(2025, 2, 3))

    # Удаляем существующую бронь
    resp_ok = api.post("/bookings/delete/", {"booking_id": b.id}, format="json")
    assert resp_ok.status_code == 200, resp_ok.content
    assert resp_ok.json() == {"status": "ok"}
    assert not Booking.objects.filter(pk=b.id).exists()

    # Повторное удаление той же — уже 404
    resp_404 = api.post("/bookings/delete/", {"booking_id": b.id}, format="json")
    assert resp_404.status_code == 404, resp_404.content
    assert resp_404.json() == {"detail": "booking not found"}
