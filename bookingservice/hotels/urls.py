
from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('rooms/create', views.create_room, name='room_create'),
    path('rooms/delete', views.delete_room, name='room_delete'),
    path("rooms/list", views.list_rooms, name='room_list'),
    path('bookings/create', views.create_booking, name='booking_create'),
    path('bookings/delete', views.delete_booking, name='booking_delete'),
    path('bookings/list', views.list_bookings, name='booking_list'),
]
