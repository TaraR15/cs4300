from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Template URLs
    path('', views.movie_list, name='movie_list'),
    path('book/<int:movie_id>/', views.seat_booking, name='seat_booking'),
    path('history/', views.booking_history, name='booking_history'),

    #testing
    path('', views.movie_list, name='movie_list'),
    path('ultra-test/<int:movie_id>/', views.ultra_simple_test, name='ultra_test'),
    path('book/<int:movie_id>/', views.seat_booking, name='seat_booking'),
]
