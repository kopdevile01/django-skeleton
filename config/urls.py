from django.contrib import admin
from django.urls import path

from hotel.views import create_room_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", create_room_view),
]
