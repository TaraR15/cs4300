from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from bookings.models import Movie, Seat, Booking
#API testing imports
from rest_framework.test import APIClient
from rest_framework import status


#---------Start of unit tests-------------
class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            release_date=date(2024, 1, 1),
            duration=120
        )
    
    def test_movie_creation(self):
        """Test that a movie is created correctly"""
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.duration, 120)
        self.assertEqual(str(self.movie), "Test Movie")
    
    def test_movie_defaults(self):
        """Test movie default values"""
        self.assertIsNotNone(self.movie.release_date)

class SeatModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.seat = Seat.objects.create(
            seat_number="A1",
            movie=self.movie,
            is_booked=False
        )
    
    def test_seat_creation(self):
        """Test that a seat is created correctly"""
        self.assertEqual(self.seat.seat_number, "A1")
        self.assertFalse(self.seat.is_booked)
        self.assertEqual(self.seat.movie, self.movie)
    
    def test_seat_string_representation(self):
        """Test the string representation of seat"""
        expected = "Seat A1 - Available"
        self.assertEqual(str(self.seat), expected)
        
        # Test booked seat string
        self.seat.is_booked = True
        self.seat.save()
        expected = "Seat A1 - Booked"
        self.assertEqual(str(self.seat), expected)

class BookingModelTest(TestCase):
    def setUp(self):
        # Create a movie
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            release_date=date(2024, 1, 1),
            duration=120
        )
        
        # Create a seat
        self.seat = Seat.objects.create(
            seat_number="A1",
            movie=self.movie,
            is_booked=False
        )
        
        # Create a booking WITHOUT a user (since user is nullable in your app)
        self.booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=None  # This matches your current setup
        )
    
    def test_booking_creation(self):
        """Test that a booking is created correctly"""
        self.assertEqual(self.booking.movie, self.movie)
        self.assertEqual(self.booking.seat, self.seat)
        self.assertIsNone(self.booking.user)  # Check that user is None
        self.assertIsNotNone(self.booking.booking_date)
    
    def test_booking_string_representation(self):
        """Test the string representation of booking"""
        self.assertIn(self.movie.title, str(self.booking))
        self.assertIn(self.seat.seat_number, str(self.booking))


#----------------Start of API tests---------------
