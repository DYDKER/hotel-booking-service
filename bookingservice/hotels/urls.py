
from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('bookings/slug/<slug:booking_slug>/', views.booking_by_slug, name='booking_by_slug'),
    path('bookings/<int:booking_id>/', views.my_bookings, name='booking_detail'),
    path("archive/<year4:year>/", views.archive, name = 'archive'),
]
