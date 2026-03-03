from rest_framework import serializers
from .models import Movie, Seat, Booking
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    movie_title = serializers.ReadOnlyField(source='movie.title')
    seat_number = serializers.ReadOnlyField(source='seat.seat_number')
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Booking
        fields = ['id', 'movie', 'seat', 'user', 'booking_date', 
                  'movie_title', 'seat_number', 'username']


