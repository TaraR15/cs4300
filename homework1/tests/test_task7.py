from task7 import get_status_code

def test_google():
    assert get_status_code("https://www.google.com") == 200