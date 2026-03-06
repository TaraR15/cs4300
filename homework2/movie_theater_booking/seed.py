#!/usr/bin/env python
"""
Seed script to populate the database with initial movie and seat data.
Run with: python seed.py
"""

import os
import django
from datetime import date

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_theater_booking.settings')
django.setup()

from bookings.models import Movie, Seat

def create_movies():
    """Create sample movies"""
    movies_data = [
        {
            'title': 'Oppenheimer',
            'description': 'The story of J. Robert Oppenheimer and the atomic bomb.',
            'release_date': date(2023, 7, 21),
            'duration': 180
        },
        {
            'title': 'Barbie',
            'description': 'Barbie suffers a crisis that leads her to question her world.',
            'release_date': date(2023, 7, 21),
            'duration': 114
        },
        {
            'title': 'Dune: Part Two',
            'description': 'Paul Atreides unites with the Fremen to seek revenge.',
            'release_date': date(2024, 3, 1),
            'duration': 166
        },
        {
            'title': 'Poor Things',
            'description': 'A young woman is brought back to life by a scientist.',
            'release_date': date(2023, 12, 8),
            'duration': 141
        }
    ]
    
    created_movies = []
    for movie_data in movies_data:
        movie, created = Movie.objects.get_or_create(
            title=movie_data['title'],
            defaults=movie_data
        )
        if created:
            print(f" Created movie: {movie.title}")
        else:
            print(f"  Movie already exists: {movie.title}")
        created_movies.append(movie)
    
    return created_movies

def create_seats_for_movie(movie):
    """Create 15 seats (A1-A5, B1-B5, C1-C5) for a movie"""
    rows = ['A', 'B', 'C']
    seats_per_row = 5
    
    created_count = 0
    for row in rows:
        for num in range(1, seats_per_row + 1):
            seat_number = f"{row}{num}"
            seat, created = Seat.objects.get_or_create(
                seat_number=seat_number,
                movie=movie,
                defaults={'is_booked': False}
            )
            if created:
                created_count += 1
    
    if created_count > 0:
        print(f"  Created {created_count} seats for {movie.title}")
    else:
        print(f"  Seats already exist for {movie.title}")

def main():
    """Main seed function"""
    print("\n Starting database seed...\n")
    
    # Create movies
    movies = create_movies()
    
    # Create seats for each movie
    print("\n Creating seats...")
    for movie in movies:
        create_seats_for_movie(movie)
    
    # Summary
    print(f"\n Summary:")
    print(f"  - Movies: {Movie.objects.count()}")
    print(f"  - Seats: {Seat.objects.count()}")
    print(f"\n Seed complete!\n")

if __name__ == '__main__':
    main()
