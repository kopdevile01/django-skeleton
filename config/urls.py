from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

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
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

SPECTACULAR_SETTINGS = {
    "TITLE": "Hotel API",
    "DESCRIPTION": "Rooms & bookings (Django + DRF)",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
