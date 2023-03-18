import requests

data = {
    'user_id':'11111',
    'client_id':'111222',
    'anime_name':'测试anime',
    'episode_num':'111222333444',
    'director':'director',
    'collection_type':'收藏',
    'rating':'114514',
    'comment':'comment_test',
}
url = 'http://localhost:8000/anime/modify_collection/s'
print(requests.post(url,data).text)