Feature: Movie Seat Booking
  As a movie enthusiast
  I want to browse movies and book seats
  So that I can watch films at the theater

  Scenario: Viewing available movies
    Given there are movies in the database
    When I visit the home page
    Then I should see a list of movies

  Scenario: Booking a seat for a movie
    Given a movie "Test Movie" exists with available seats
    When I navigate to the seat booking page for that movie
    Then I should see available seats
    And I should see the movie details

  Scenario: Successfully booking a seat
    Given I am on the seat booking page for "Test Movie"
    When I select and book an available seat
    Then the seat should become booked
    And I should see a success message
