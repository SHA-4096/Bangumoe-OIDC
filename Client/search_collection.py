import requests
anime_name = 'anime'
data = {
    'user_id':'11111',
    'anime_name':anime_name,
    'client_id':'111222'
}
url = 'http://localhost:8000/anime/search_collection/s'
print(requests.get(url,data).text)