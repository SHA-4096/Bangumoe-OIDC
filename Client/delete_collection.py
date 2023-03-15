import requests

data = {
    'user_id':'11111',
    'anime_name':'测试anime',
}
url = 'http://localhost:8000/anime/delete_collection/s'
print(requests.get(url,data).text)