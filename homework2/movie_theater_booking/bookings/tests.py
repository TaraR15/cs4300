from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from bookings.models import Movie, Seat, Booking
#API testing imports
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


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
class MovieAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title="API Test Movie",
            description="Test Description",
            release_date=date(2024, 1, 1),
            duration=120
        )
    
    def test_get_movies_list(self):
        """Test GET /api/movies/"""
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_single_movie(self):
        """Test GET /api/movies/{id}/"""
        response = self.client.get(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "API Test Movie")

class SeatAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
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
    
    def test_get_seats_list(self):
        """Test GET /api/seats/"""
        response = self.client.get('/api/seats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
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
        self.booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=None
        )
    
    def test_get_bookings_list(self):
        """Test GET /api/bookings/"""
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_booking(self):
        """Test POST /api/bookings/"""
        new_seat = Seat.objects.create(
            seat_number="A2",
            movie=self.movie,
            is_booked=False
        )
        data = {
            'movie': self.movie.id,
            'seat': new_seat.id,
            'user': None
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
