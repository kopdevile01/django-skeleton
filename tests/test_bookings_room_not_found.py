import pytest


@pytest.mark.django_db
def test_bookings_create_returns_404_for_missing_room(api):
    payload = {
        "room_id": 999_999,  # заведомо несуществующий id
        "date_start": "2025-12-30",
        "date_end": "2026-01-02",
    }
    resp = api.post("/bookings/create/", payload, format="json")

    assert resp.status_code == 404, resp.content
    assert resp.json() == {"detail": "room not found"}
