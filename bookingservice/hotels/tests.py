from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Booking, HotelRoom


class HotelModelsTests(TestCase):
    def test_hotel_room_stores_description_price_and_created_at(self):
        room = HotelRoom.objects.create(
            description="Sea view room",
            price_per_night=Decimal("5000.00"),
        )

        self.assertEqual(room.description, "Sea view room")
        self.assertEqual(room.price_per_night, Decimal("5000.00"))
        self.assertIsNotNone(room.created_at)
        self.assertEqual(str(room), f"Room {room.id}: Sea view room")

    def test_booking_belongs_to_room_and_is_deleted_with_room(self):
        room = HotelRoom.objects.create(
            description="Small room",
            price_per_night=Decimal("2500.00"),
        )
        booking = Booking.objects.create(
            room=room,
            date_start=date(2026, 7, 20),
            date_end=date(2026, 7, 25),
        )

        self.assertEqual(booking.room, room)
        self.assertEqual(str(booking), f"Booking {booking.id} for room {room.id}")

        room.delete()

        self.assertFalse(Booking.objects.filter(id=booking.id).exists())


class BookingPagesTests(TestCase):
    def test_home_page_uses_hotel_booking_copy(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Hotel Booking Service")

    def test_booking_detail_page_uses_booking_id(self):
        response = self.client.get(reverse("booking_detail", args=(12,)))

        self.assertContains(response, "My Bookings")
        self.assertContains(response, "id: 12")

    def test_booking_slug_page_uses_booking_slug(self):
        response = self.client.get(reverse("booking_by_slug", args=("sea-view-room",)))

        self.assertContains(response, "My Bookings")
        self.assertContains(response, "slug: sea-view-room")

    def test_future_archive_redirects_to_booking_slug_page(self):
        response = self.client.get(reverse("archive", args=(2027,)))

        self.assertRedirects(response, reverse("booking_by_slug", args=("tracking",)))
