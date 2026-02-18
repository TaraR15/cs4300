import requests

def get_status_code(url):
    response = requests.get(url)
    return response.status_code