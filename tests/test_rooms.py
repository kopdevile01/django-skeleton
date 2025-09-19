from decimal import Decimal

from hotel.models import Room


def test_create_room_returns_id_and_persists(api, db):
    resp = api.post(
        "/rooms/",
        {"description": "Economy double", "price": "99.99"},
        format="json",
    )

    assert resp.status_code == 201
    assert "room_id" in resp.data
    rid = resp.data["room_id"]
    assert isinstance(rid, int)

    room = Room.objects.get(pk=rid)
    assert room.description == "Economy double"
    assert room.price == Decimal("99.99")
