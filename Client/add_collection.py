import requests

data = {
    'user_id':'11111',
    'client_id':'111222',
    'anime_name':'anime_name',
    'episode_num':'100',
    'director':'director',
    'collection_type':'收藏',
    'rating':'100',
    'comment':'这是一条关于猪猪掉进青年园池子里的comment',
}
url = 'http://localhost:8000/anime/collect_anime/s'
print(requests.post(url,data).text)