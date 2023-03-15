import requests

data = {
    'user_id':'11111',
}
url = 'http://localhost:8000/anime/view_collections/s'
print(requests.get(url,data).text)