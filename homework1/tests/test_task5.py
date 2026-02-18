import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from task5 import favorite_books, student_database

def test_books():
    books = favorite_books()
    assert len(books) == 3
    assert books[0]["title"] == "Two Twisted Crowns"

def test_database():
    db = student_database()
    assert db["Hugh Janus"] == 1001