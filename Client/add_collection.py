import requests

data = {
    'user_id':'11111',
    'anime_name':'测试anime',
    'episode_num':'114514',
    'director':'director',
    'collection_type':'收藏',
    'rating':'114514',
    'comment':'comment_test',
}
url = 'http://localhost:8000/anime/collect_anime/s'
print(requests.post(url,data).text)