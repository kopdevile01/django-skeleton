from django.contrib import admin
from django.urls import path

from hotel.views import rooms_collection

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", rooms_collection),
]
