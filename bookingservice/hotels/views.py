from datetime import date
from decimal import Decimal, InvalidOperation

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from hotels.models import Booking, HotelRoom


def index(request):
    return HttpResponse("<h1>Hotel Booking Service</h1>")


def my_bookings(request, booking_id=None):
    if booking_id is None:
        return HttpResponse("<h1>My Bookings</h1>")

    return HttpResponse(f"<h1>My Bookings</h1><p>id: {booking_id}</p>")


def booking_by_slug(request, booking_slug):
    if request.GET:
        print(request.GET)

    return HttpResponse(f"<h1>My Bookings</h1><p>slug: {booking_slug}</p>")


def archive(request, year):
    if year > 2026:
        uri = reverse("booking_by_slug", args=("tracking",))
        return HttpResponseRedirect(uri)

    return HttpResponse(f"<h1>Booking archive by year</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Booking page not found</h1>")


def error_response(message, status=400):
    return JsonResponse({"error": message}, status=status)


@csrf_exempt
def create_room(request):
    if request.method != "POST":
        return error_response("method not allowed", 405)

    description = request.POST.get("description", "").strip()
    price_per_night = request.POST.get("price_per_night")

    if not description:
        return error_response("description is required")

    try:
        price_per_night = Decimal(price_per_night)
    except (InvalidOperation, TypeError):
        return error_response("price_per_night must be a number")

    if price_per_night <= 0:
        return error_response("price_per_night must be positive")

    room = HotelRoom.objects.create(
        description=description,
        price_per_night=price_per_night,
    )

    return JsonResponse({"room_id": room.id})


@csrf_exempt
def delete_room(request):
    if request.method != "POST":
        return error_response("method not allowed", 405)

    try:
        room = HotelRoom.objects.get(id=int(request.POST.get("room_id", "")))
    except ValueError:
        return error_response("room_id must be an integer")
    except HotelRoom.DoesNotExist:
        return error_response("room not found", 404)

    room.delete()
    return JsonResponse({"deleted": True})


def list_rooms(request):
    if request.method != "GET":
        return error_response("method not allowed", 405)

    sort_map = {
        "price": "price_per_night",
        "created_at": "created_at",
    }
    sort_by = request.GET.get("sort_by")
    order = request.GET.get("order", "asc")

    if sort_by and sort_by not in sort_map:
        return error_response("sort_by must be price or created_at")
    if order not in ("asc", "desc"):
        return error_response("order must be asc or desc")

    order_by = sort_map.get(sort_by, "id")
    if order == "desc":
        order_by = f"-{order_by}"

    rooms = HotelRoom.objects.order_by(order_by)
    data = [
        {
            "room_id": room.id,
            "description": room.description,
            "price_per_night": str(room.price_per_night),
            "created_at": room.created_at.isoformat(),
        }
        for room in rooms
    ]

    return JsonResponse(data, safe=False)


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


@csrf_exempt
def create_booking(request):
    if request.method != "POST":
        return error_response("method not allowed", 405)

    try:
        room = HotelRoom.objects.get(id=int(request.POST.get("room_id", "")))
    except ValueError:
        return error_response("room_id must be an integer")
    except HotelRoom.DoesNotExist:
        return error_response("room not found", 404)

    date_start = parse_date(request.POST.get("date_start"))
    date_end = parse_date(request.POST.get("date_end"))
    if date_start is None or date_end is None:
        return error_response("dates must use YYYY-MM-DD format")
    if date_end <= date_start:
        return error_response("date_end must be after date_start")

    booking = Booking.objects.create(
        room=room,
        date_start=date_start,
        date_end=date_end,
    )
    return JsonResponse({"booking_id": booking.id})


@csrf_exempt
def delete_booking(request):
    if request.method != "POST":
        return error_response("method not allowed", 405)

    try:
        booking = Booking.objects.get(id=int(request.POST.get("booking_id", "")))
    except ValueError:
        return error_response("booking_id must be an integer")
    except Booking.DoesNotExist:
        return error_response("booking not found", 404)

    booking.delete()
    return JsonResponse({"deleted": True})


def list_bookings(request):
    if request.method != "GET":
        return error_response("method not allowed", 405)

    try:
        room = HotelRoom.objects.get(id=int(request.GET.get("room_id", "")))
    except ValueError:
        return error_response("room_id must be an integer")
    except HotelRoom.DoesNotExist:
        return error_response("room not found", 404)

    bookings = Booking.objects.filter(room=room).order_by("date_start")
    data = [
        {
            "booking_id": booking.id,
            "date_start": booking.date_start.isoformat(),
            "date_end": booking.date_end.isoformat(),
        }
        for booking in bookings
    ]
    return JsonResponse(data, safe=False)
