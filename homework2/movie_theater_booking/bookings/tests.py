from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
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

    def test_movie_with_empty_description(self):
        """Test movie can be created with empty description"""
        movie = Movie.objects.create(
            title="No Description",
            description="",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.assertEqual(movie.description, "")

    def test_movie_with_very_long_title(self):
        """Test movie with very long title (edge case)"""
        long_title = "A" * 255  # Max length
        movie = Movie.objects.create(
            title=long_title,
            description="Test",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.assertEqual(len(movie.title), 255)

    def test_movie_with_zero_duration(self):
        """Test edge case: movie with 0 duration"""
        movie = Movie.objects.create(
            title="Zero Duration",
            description="Test",
            release_date=date(2024, 1, 1),
            duration=0
        )
        self.assertEqual(movie.duration, 0)

    def test_movie_with_future_release_date(self):
        """Test movie with future release date"""
        future_date = date.today() + timedelta(days=365)
        movie = Movie.objects.create(
            title="Future Movie",
            description="Test",
            release_date=future_date,
            duration=120
        )
        self.assertEqual(movie.release_date, future_date)
    
    

class SeatModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            release_date=date(2024, 1, 1),
            duration=120
        )
        # Don't create a default seat here so each test create what it needs and operate independently
    
    def test_seat_creation(self):
        """Test that a seat is created correctly"""
        seat = Seat.objects.create(
            seat_number="A1",
            movie=self.movie,
            is_booked=False
        )
        self.assertEqual(seat.seat_number, "A1")
        self.assertFalse(seat.is_booked)
        self.assertEqual(seat.movie, self.movie)
    
    def test_seat_string_representation(self):
        """Test the string representation of seat"""
        seat = Seat.objects.create(
            seat_number="A1",
            movie=self.movie,
            is_booked=False
        )
        expected = "Seat A1 - Available"
        self.assertEqual(str(seat), expected)
        
        # Test booked seat string
        seat.is_booked = True
        seat.save()
        expected = "Seat A1 - Booked"
        self.assertEqual(str(seat), expected)

    def test_duplicate_seat_number_different_movies(self):
        """Test same seat number allowed for different movies"""
        movie1 = Movie.objects.create(title="Movie 1", release_date=date.today(), duration=120)
        movie2 = Movie.objects.create(title="Movie 2", release_date=date.today(), duration=120)
        
        # Create seats for different movies
        seat1 = Seat.objects.create(seat_number="A1", movie=movie1)
        seat2 = Seat.objects.create(seat_number="A1", movie=movie2)
        
        # Count should be 2 (the two just created)
        self.assertEqual(Seat.objects.filter(seat_number="A1").count(), 2)

    def test_cannot_create_duplicate_seat_same_movie(self):
        """Test cannot create duplicate seat number for same movie"""
        # Create first seat
        Seat.objects.create(seat_number="A1", movie=self.movie)
        
        # Try to create duplicate - should raise an exception
        with self.assertRaises(Exception):
            Seat.objects.create(seat_number="A1", movie=self.movie)

    def test_booking_already_booked_seat(self):
        """Test trying to book an already booked seat"""
        # Create a seat that's already booked
        seat = Seat.objects.create(
            seat_number="B1",
            movie=self.movie,
            is_booked=True
        )
        
        # Try to create booking for booked seat, this should NOT raise an exception
        # because app allows creating bookings for booked seats (the seat just stays booked)
        try:
            Booking.objects.create(
                movie=self.movie,
                seat=seat,
                user=None
            )
            # If we get here, no exception was raised
            booking_exists = Booking.objects.filter(seat=seat).exists()
            self.assertTrue(booking_exists)
        except Exception:
            self.fail("Booking creation raised an exception when it shouldn't")

    def test_booking_same_seat_twice(self):
        """Test booking the same seat twice"""
        # Create a seat
        seat = Seat.objects.create(
            seat_number="B2",
            movie=self.movie,
            is_booked=False
        )
        
        # First booking
        booking1 = Booking.objects.create(movie=self.movie, seat=seat, user=None)
        seat.refresh_from_db()
        
        # booking a seat doesn't automatically mark it as booked
        # The seat.is_booked field might need to be updated separately
        self.assertEqual(Booking.objects.filter(seat=seat).count(), 1)
        
        # Second booking
        booking2 = Booking.objects.create(movie=self.movie, seat=seat, user=None)
        self.assertEqual(Booking.objects.filter(seat=seat).count(), 2)


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
        
        # Create a booking WITHOUT a user (since user is nullable)
        self.booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=None
        )
    
    def test_booking_creation(self):
        """Test that a booking is created correctly"""
        self.assertEqual(self.booking.movie, self.movie)
        self.assertEqual(self.booking.seat, self.seat)
        self.assertIsNone(self.booking.user)
        self.assertIsNotNone(self.booking.booking_date)
    
    def test_booking_string_representation(self):
        """Test the string representation of booking"""
        self.assertIn(self.movie.title, str(self.booking))
        self.assertIn(self.seat.seat_number, str(self.booking))

    def test_booking_without_movie(self):
        """Test booking cannot be created without a movie"""
        seat = Seat.objects.create(seat_number="A2", movie=self.movie)
        with self.assertRaises(Exception):
            Booking.objects.create(seat=seat, user=None)

    def test_booking_without_seat(self):
        """Test booking cannot be created without a seat"""
        with self.assertRaises(Exception):
            Booking.objects.create(movie=self.movie, user=None)

    def test_multiple_bookings_different_seats(self):
        """Test user can book multiple different seats"""
        seat1 = Seat.objects.create(seat_number="A2", movie=self.movie)
        seat2 = Seat.objects.create(seat_number="A3", movie=self.movie)
        
        Booking.objects.create(movie=self.movie, seat=seat1, user=None)
        Booking.objects.create(movie=self.movie, seat=seat2, user=None)
        
        self.assertEqual(Booking.objects.count(), 3)  # Including the one from setUp


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

    def test_get_nonexistent_movie(self):
        """Test GET for movie that doesn't exist"""
        response = self.client.get('/api/movies/999/')
        self.assertEqual(response.status_code, 404)
    
    def test_create_movie_with_invalid_data(self):
        """Test POST with missing required fields"""
        invalid_data = {
            'title': 'Invalid Movie'
            # Missing description, release_date, duration
        }
        response = self.client.post('/api/movies/', invalid_data, format='json')
        self.assertEqual(response.status_code, 400)


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

    def test_create_booking_with_invalid_seat(self):
        """Test booking with seat that doesn't exist"""
        data = {
            'movie': self.movie.id,
            'seat': 999,
            'user': None
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, 400)