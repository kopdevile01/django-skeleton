from datetime import date

import pytest

from hotel.models import Booking, Room


@pytest.mark.django_db
def test_bookings_list_sorted_by_date_start(api):
    room = Room.objects.create(description="Sort room", price="10.00")
    # создаём в «перемешанном» порядке
    Booking.objects.create(room=room, date_start=date(2025, 1, 10), date_end=date(2025, 1, 12))
    Booking.objects.create(room=room, date_start=date(2025, 1, 5), date_end=date(2025, 1, 8))
    Booking.objects.create(room=room, date_start=date(2025, 1, 7), date_end=date(2025, 1, 9))

    resp = api.get(f"/bookings/list/?room_id={room.id}")
    assert resp.status_code == 200, resp.content
    data = resp.json()

    # должно быть отсортировано по date_start ASC
    assert [b["date_start"] for b in data] == ["2025-01-05", "2025-01-07", "2025-01-10"]
