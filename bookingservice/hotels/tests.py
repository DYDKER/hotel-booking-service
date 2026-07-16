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


class RoomApiTests(TestCase):
    def test_create_room_returns_room_id(self):
        response = self.client.post(
            reverse("room_create"),
            {
                "description": "Sea view room",
                "price_per_night": "5000.00",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = response.json()
        self.assertIn("room_id", data)

        room = HotelRoom.objects.get(id=data["room_id"])
        self.assertEqual(room.description, "Sea view room")
        self.assertEqual(room.price_per_night, Decimal("5000.00"))

    def test_create_room_requires_description(self):
        response = self.client.post(
            reverse("room_create"),
            {"price_per_night": "5000.00"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "description is required"})
        self.assertEqual(HotelRoom.objects.count(), 0)

    def test_create_room_requires_positive_price(self):
        response = self.client.post(
            reverse("room_create"),
            {
                "description": "Sea view room",
                "price_per_night": "0",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "price_per_night must be positive"})
        self.assertEqual(HotelRoom.objects.count(), 0)

    def test_create_room_requires_valid_price(self):
        response = self.client.post(
            reverse("room_create"),
            {
                "description": "Sea view room",
                "price_per_night": "not-a-number",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "price_per_night must be a number"})
        self.assertEqual(HotelRoom.objects.count(), 0)

    def test_list_rooms_returns_rooms_sorted_by_id_by_default(self):
        first_room = HotelRoom.objects.create(
            description="First room",
            price_per_night=Decimal("3000.00"),
        )
        second_room = HotelRoom.objects.create(
            description="Second room",
            price_per_night=Decimal("2000.00"),
        )

        response = self.client.get(reverse("room_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "room_id": first_room.id,
                    "description": "First room",
                    "price_per_night": "3000.00",
                    "created_at": first_room.created_at.isoformat(),
                },
                {
                    "room_id": second_room.id,
                    "description": "Second room",
                    "price_per_night": "2000.00",
                    "created_at": second_room.created_at.isoformat(),
                },
            ],
        )

    def test_list_rooms_sorts_by_price_desc(self):
        cheap_room = HotelRoom.objects.create(
            description="Cheap room",
            price_per_night=Decimal("1000.00"),
        )
        expensive_room = HotelRoom.objects.create(
            description="Expensive room",
            price_per_night=Decimal("9000.00"),
        )

        response = self.client.get(
            reverse("room_list"),
            {"sort_by": "price", "order": "desc"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [room["room_id"] for room in response.json()],
            [expensive_room.id, cheap_room.id],
        )

    def test_list_rooms_rejects_unknown_sort_field(self):
        response = self.client.get(reverse("room_list"), {"sort_by": "description"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "sort_by must be price or created_at"})

    def test_delete_room_removes_room_and_its_bookings(self):
        room = HotelRoom.objects.create(
            description="Sea view room",
            price_per_night=Decimal("5000.00"),
        )
        booking = Booking.objects.create(
            room=room,
            date_start=date(2026, 7, 20),
            date_end=date(2026, 7, 25),
        )

        response = self.client.post(reverse("room_delete"), {"room_id": str(room.id)})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"deleted": True})
        self.assertFalse(HotelRoom.objects.filter(id=room.id).exists())
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())

    def test_delete_room_returns_404_for_unknown_room(self):
        response = self.client.post(reverse("room_delete"), {"room_id": "999"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "room not found"})
