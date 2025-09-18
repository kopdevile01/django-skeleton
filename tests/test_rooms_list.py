import pytest

from hotel.models import Room


@pytest.mark.django_db
def test_rooms_list_default_order(api):
    r1 = Room.objects.create(description="Economy", price="50.00")
    r2 = Room.objects.create(description="Deluxe", price="250.00")

    resp = api.get("/rooms/")
    assert resp.status_code == 200, resp.content

    data = resp.json()
    # по умолчанию created_at ASC -> сначала r1, потом r2
    assert [item["id"] for item in data] == [r1.id, r2.id]
