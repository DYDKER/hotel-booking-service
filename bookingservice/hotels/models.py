from django.db import models

class HotelRoom(models.Model):
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.id}: {self.description}"

class Booking(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} for room {self.room_id}"