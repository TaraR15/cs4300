from django.contrib import admin
from .models import Movie, Seat, Booking

# Register your models here

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration')
    search_fields = ('title',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'is_booked')
    list_filter = ('is_booked',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'seat', 'user', 'booking_date')
    list_filter = ('booking_date',)
    date_hierarchy = 'booking_date'


