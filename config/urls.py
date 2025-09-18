from django.contrib import admin
from django.urls import path

from hotel.views import (
    bookings_create,
    bookings_delete,
    bookings_list,
    rooms_collection,
    rooms_item,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", rooms_collection),
    path("rooms/<int:room_id>/", rooms_item),
    path("bookings/create/", bookings_create),
    path("bookings/list/", bookings_list),
    path("bookings/delete/", bookings_delete),
]
