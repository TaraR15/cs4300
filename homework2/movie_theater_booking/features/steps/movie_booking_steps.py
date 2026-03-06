from behave import given, when, then
from django.urls import reverse
from bookings.models import Movie, Seat, Booking
from datetime import date

@given('there are movies in the database')
def step_impl(context):
    Movie.objects.create(
        title="Inception",
        description="A thief who steals corporate secrets through dream-sharing technology.",
        release_date=date(2010, 7, 16),
        duration=148
    )
    Movie.objects.create(
        title="The Matrix",
        description="A computer hacker learns about the true nature of reality.",
        release_date=date(1999, 3, 31),
        duration=136
    )

@when('I visit the home page')
def step_impl(context):
    context.response = context.test.client.get('/')

@then('I should see a list of movies')
def step_impl(context):
    assert context.response.status_code == 200
    content = str(context.response.content)
    assert 'Inception' in content
    assert 'The Matrix' in content

@given('a movie "{title}" exists with available seats')
def step_impl(context, title):
    context.movie = Movie.objects.create(
        title=title,
        description="Test Description",
        release_date=date.today(),
        duration=120
    )
    # Create seats for this movie
    for row in ['A', 'B', 'C']:
        for num in range(1, 6):
            Seat.objects.create(
                seat_number=f"{row}{num}",
                movie=context.movie,
                is_booked=False
            )

@when('I navigate to the seat booking page for that movie')
def step_impl(context):
    url = reverse('seat_booking', args=[context.movie.id])
    context.response = context.test.client.get(url)

@then('I should see available seats')
def step_impl(context):
    content = str(context.response.content)
    assert 'A1' in content
    assert 'B1' in content
    assert 'C1' in content

@then('I should see the movie details')
def step_impl(context):
    content = str(context.response.content)
    assert context.movie.title in content
    assert context.movie.description in content

@given('I am on the seat booking page for "{title}"')
def step_impl(context, title):
    # Create the movie and seats for this scenario
    context.movie = Movie.objects.create(
        title=title,
        description="Test Description for booking",
        release_date=date.today(),
        duration=120
    )
    # Create seats
    for row in ['A', 'B', 'C']:
        for num in range(1, 6):
            Seat.objects.create(
                seat_number=f"{row}{num}",
                movie=context.movie,
                is_booked=False
            )
    
    # Visit the seat booking page
    url = reverse('seat_booking', args=[context.movie.id])
    context.response = context.test.client.get(url)
    
    # Store an available seat for later
    context.seat = Seat.objects.filter(movie=context.movie, is_booked=False).first()

@when('I select and book an available seat')
def step_impl(context):
    context.response = context.test.client.post(
        reverse('seat_booking', args=[context.movie.id]),
        {'seat_id': context.seat.id}
    )
    # Follow with a GET to see the result
    context.follow_response = context.test.client.get(
        reverse('seat_booking', args=[context.movie.id])
    )

@then('the seat should become booked')
def step_impl(context):
    context.seat.refresh_from_db()
    assert context.seat.is_booked is True

@then('I should see a success message')
def step_impl(context):
    content = str(context.follow_response.content)
    assert 'Successfully booked' in content or 'success' in content.lower()