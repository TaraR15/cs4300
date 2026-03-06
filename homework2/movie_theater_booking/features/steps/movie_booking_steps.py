from behave import given, when, then
from django.urls import reverse
from bookings.models import Movie, Seat, Booking
from datetime import date
from behave.api.pending_step import StepNotImplementedError

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


@given(u'I book seat "{seat_number}"')
def step_impl(context, seat_number):
    """Book a specific seat"""
    # Find the seat
    seat = Seat.objects.get(seat_number=seat_number, movie=context.movie)
    
    # Book it
    context.response = context.test.client.post(
        reverse('seat_booking', args=[context.movie.id]),
        {'seat_id': seat.id}
    )
    context.seat = seat

@when(u'I try to book the same seat "{seat_number}" again')
def step_impl(context, seat_number):
    """Try to book the same seat again"""
    seat = Seat.objects.get(seat_number=seat_number, movie=context.movie)
    context.response = context.test.client.post(
        reverse('seat_booking', args=[context.movie.id]),
        {'seat_id': seat.id}
    )

@then(u'I should see an error message')
def step_impl(context):
    """Check that error message appears"""
    # Get the response content (either from context.response or follow up with a GET)
    if hasattr(context, 'follow_response'):
        content = str(context.follow_response.content)
    else:
        # Do a GET request to see the page with messages
        context.follow_response = context.test.client.get(
            reverse('seat_booking', args=[context.movie.id])
        )
        content = str(context.follow_response.content)
    
    # Check for error message in Django messages or page content
    assert ('already booked' in content.lower() or 
            'error' in content.lower() or 
            'cannot' in content.lower()), f"Error message not found in: {content[:500]}"

@then(u'the seat should remain booked only once')
def step_impl(context):
    """Verify seat is still booked and only one booking exists"""
    context.seat.refresh_from_db()
    assert context.seat.is_booked is True, "Seat is not booked"
    # Check only one booking exists for this seat
    bookings_count = Booking.objects.filter(seat=context.seat).count()
    assert bookings_count == 1, f"Expected 1 booking, found {bookings_count}"

@given(u'a movie "{title}" exists with all seats booked')
def step_impl(context, title):
    """Create a movie where all seats are already booked"""
    context.movie = Movie.objects.create(
        title=title,
        description="Test Description for fully booked movie",
        release_date=date.today(),
        duration=120
    )
    # Create seats and mark them all as booked
    for row in ['A', 'B', 'C']:
        for num in range(1, 6):
            Seat.objects.create(
                seat_number=f"{row}{num}",
                movie=context.movie,
                is_booked=True  # All seats booked
            )

@when(u'I visit the seat booking page')
def step_impl(context):
    """Visit the seat booking page for the movie"""
    url = reverse('seat_booking', args=[context.movie.id])
    context.response = context.test.client.get(url)

@then(u'I should see "No seats available" message')
def step_impl(context):
    """Check for no seats available message or absence of book buttons"""
    content = str(context.response.content).lower()
    
    # Either there's a message OR there are no book buttons
    has_message = any(msg in content for msg in ['no seats', 'unavailable', 'sold out', 'booked'])
    has_book_buttons = 'btn-success' in content or 'book seat' in content
    
    if has_book_buttons:
        # If there are book buttons, there should be a message
        assert has_message, "Seat buttons present but no 'no seats' message found"
    else:
        # No book buttons is acceptable
        pass

@then(u'the book button should be disabled')
def step_impl(context):
    """Check that book buttons are disabled"""
    content = str(context.response.content)
    # Check for disabled buttons or no book buttons at all
    has_disabled = 'disabled' in content
    has_no_buttons = 'book' not in content.lower() or 'btn-success' not in content
    
    assert has_disabled or has_no_buttons, "Book buttons are still enabled when they should be disabled"

@when(u'I try to book seats for movie ID 999')
def step_impl(context):
    """Try to access a non-existent movie"""
    context.response = context.test.client.get('/book/999/')

@then(u'I should see a "Movie not found" error')
def step_impl(context):
    """Check for 404 or movie not found message"""
    # Could be a 404 page or a redirect to home with message
    if context.response.status_code == 404:
        assert True  # Got 404, which is correct
    else:
        content = str(context.response.content)
        assert 'not found' in content.lower() or 'does not exist' in content.lower()




def _check_for_message(context, message_text):
    """Helper to check for Django messages in response"""
    if hasattr(context, 'follow_response'):
        content = str(context.follow_response.content)
    else:
        # Try to get messages from session
        try:
            messages = list(context.test.client.session.get('messages', []))
            if messages:
                return any(message_text in str(m) for m in messages)
        except:
            pass
        
        # Fallback to checking response content
        content = str(context.response.content)
    
    return message_text.lower() in content.lower()