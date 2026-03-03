from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
# Create your views here.

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

# API Views
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        seat = self.get_object()
        if seat.is_booked:
            return Response({'error': 'Seat already booked'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        seat.is_booked = True
        seat.save()
        return Response({'status': 'seat booked'})

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Booking.objects.all()
    
    def get_queryset(self):
        # Users can only see their own bookings
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Auto-assign the current user
        serializer.save(user=self.request.user)

# Template Views
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

def seat_booking(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    seats = Seat.objects.all()
    return render(request, 'bookings/seat_booking.html', {
        'movie': movie,
        'seats': seats
    })

def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})

