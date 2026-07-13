from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse


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
