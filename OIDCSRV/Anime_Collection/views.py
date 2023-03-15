from django.shortcuts import render,HttpResponse,redirect
from Anime_Collection.models import AnimeCollectionData
# Create your views here.

def collect_anime(request):
    if request.method == 'POST':
        data = {
            'user_id':request.POST['user_id'],
            'anime_name':request.POST['anime_name'],
            'episode_num':request.POST['episode_num'],
            'director':request.POST['director'],
            'collection_type':request.POST['collection_type'],
            'rating':request.POST['rating'],
            'comment':request.POST['comment'],
        }
        res = AnimeCollectionData.objects.filter(user_id=data['user_id'],anime_name=data['anime_name']).first()
        #先检查是否已经收藏
        if res:
            return HttpResponse("您已经收藏了这部番哦！")
        else:
            tmp = AnimeCollectionData(user_id=data['user_id'],anime_name=data['anime_name'],\
                episode_num=data['episode_num'],director=data['director'],\
                    collection_type=data['collection_type'],rating=data['rating'],comment=data['comment'])
            tmp.save()
            return HttpResponse("收藏成功")
    else:
        return HttpResponse("请使用POST方法")

def modify_collection(request):
    if request.method == 'POST':
        data = {
            'user_id':request.POST['user_id'],
            'anime_name':request.POST['anime_name'],
            'episode_num':request.POST['episode_num'],
            'director':request.POST['director'],
            'collection_type':request.POST['collection_type'],
            'rating':request.POST['rating'],
            'comment':request.POST['comment'],
        }
        res = AnimeCollectionData.objects.filter(user_id=data['user_id'],anime_name=data['anime_name']).first()
        if res:
            res.director = data['director']
            res.collection_type = data['collection_type']
            res.rating = data['rating']
            res.comment = data['comment']
            res.episode_num = data['episode_num']
            res.save()
            return HttpResponse("修改成功")
        else:
            return HttpResponse("用户没有收藏该番剧")
    else:
        return HttpResponse("请使用POST方法")

def delete_collection(request):
    if request.method == 'GET':
        data = {
            'user_id':request.GET['user_id'],
            'anime_name':request.GET['anime_name'],
        }
        res = AnimeCollectionData.objects.filter(user_id=data['user_id'],anime_name=data['anime_name']).first()
        if res:
            res.delete()
            return HttpResponse("删除成功")
        else:
            return HttpResponse("您并没有收藏这部番剧")
    else:
        return HttpResponse("请使用GET方法")
    
def search_collection(request):
    if request.method == 'GET':
        data = {
            'user_id':request.GET['user_id'],
            'anime_name':request.GET['anime_name'],
        }
        res = AnimeCollectionData.objects.filter(user_id=data['user_id'],anime_name=data['anime_name']).first()
        if res:
            collected = res.anime_name
            url = 'http://localhost:8000/anime/collection_data/s?user_id='+res.user_id+'&anime_name='+res.anime_name
            context = {
                'collected':collected,
                'url':url,
            }
            return HttpResponse(str(context))
    else:
        return HttpResponse("请使用GET方法")
    
def view_collections(request):
    if request.method == 'GET':
        data = {
            'user_id':request.GET['user_id'],
        }
        res = AnimeCollectionData.objects.filter(user_id=data['user_id'])
        collected = []
        urls = []
        for i in res:
            collected.append(i.anime_name)
            urls.append('http://localhost:8000/anime/collection_data/s?user_id='+i.user_id+'&anime_name='+i.anime_name)
        context={
            'collected':collected,
            'urls':urls
        }
        return HttpResponse(str(context))
#        return render(request,'all_collections.html',context=context)#后续做个网页链接的生成
    else:
        return HttpResponse("请使用GET方法")

def collection_data(request):
    if request.method == 'GET':
        data = {
            'user_id':request.GET['user_id'],
            'anime_name':request.GET['anime_name'],
        }
        res = AnimeCollectionData.objects.filter(anime_name=data['anime_name']).first()
        context = {
            'anime_name':res.anime_name,
            'episode_num':res.episode_num,
            'director':res.director,
            'collection_type':res.collection_type,
            'rating':res.rating,
            'comment':res.comment,
        }
        return HttpResponse(str(context))
    else:
        return HttpResponse("请使用GET方法")
