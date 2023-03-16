import requests

data = {
    'user_id':'11111',
    'client_id':'111222',
    'anime_name':'anime_name',
}
url = 'http://localhost:8000/anime/delete_collection/s'
print(requests.get(url,data).text)