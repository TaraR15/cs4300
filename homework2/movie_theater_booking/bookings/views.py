from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from django.http import HttpResponse
from .models import Movie, Seat
from django.utils import timezone
from django.contrib import messages

from django.http import HttpResponse

def ultra_simple_test(request, movie_id):
    return HttpResponse(f"""
    <html>
        <head><title>ULTRA SIMPLE TEST</title></head>
        <body style="background-color: #33cc33; margin: 0; padding: 50px; font-family: Arial;">
            <div style="background-color: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                <h1 style="color: #cc0000;">✅ ULTRA SIMPLE TEST PAGE</h1>
                <p style="font-size: 20px;"><strong>Movie ID:</strong> {movie_id}</p>
                <p><strong>Timestamp:</strong> {__import__('datetime').datetime.now()}</p>
                <p><strong>Django is working!</strong></p>
                <p><a href="/" style="background-color: #333; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Back to Movies</a></p>
            </div>
        </body>
    </html>
    """)

# API Views - no authentication required
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Template Views - no login required
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})


def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    # Filter seats for this specific movie
    seats = Seat.objects.filter(movie=movie)
    
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        seat = get_object_or_404(Seat, id=seat_id, movie=movie)  # Ensure seat belongs to this movie
        
        if not seat.is_booked:
            booking = Booking.objects.create(
                movie=movie,
                seat=seat,
                user=None,
                booking_date=timezone.now()
            )
            seat.is_booked = True
            seat.save()
            messages.success(request, f'Successfully booked seat {seat.seat_number} for {movie.title}!')
        else:
            messages.error(request, f'Seat {seat.seat_number} is already booked!')
        
        return redirect('seat_booking', movie_id=movie.id)
    
    return render(request, 'bookings/seat_booking.html', {
        'movie': movie,
        'seats': seats
    })

def booking_history(request):
    # Show all bookings 
    bookings = Booking.objects.all().order_by('-booking_date')[:20]
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})