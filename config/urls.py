from django.contrib import admin
from django.urls import path

from hotel.views import rooms_collection, rooms_item

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", rooms_collection),
    path("rooms/<int:room_id>/", rooms_item),
]
