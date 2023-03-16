from django.shortcuts import render,HttpResponse,redirect
from Anime_Collection.models import AnimeCollectionData
import requests
# Create your views here.

def usr_check(user_id,client_id):
    '''检查用户的在线状态'''
    url = 'http://localhost:8000/check_online_state/s?name='+user_id+'&client_id='+client_id
    res = requests.get(url).text
    if res == 'True':
        return True
    else:
        return False

def collect_anime(request):
    if request.method == 'POST':
        data = {
            'user_id':request.POST['user_id'],
            'client_id':request.POST['client_id'],
            'anime_name':request.POST['anime_name'],
            'episode_num':request.POST['episode_num'],
            'director':request.POST['director'],
            'collection_type':request.POST['collection_type'],
            'rating':request.POST['rating'],
            'comment':request.POST['comment'],
        }
        if usr_check(data['user_id'],data['client_id']):
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
            return HttpResponse("用户认证失败，是不是没有登录？")
    else:
        return HttpResponse("请使用POST方法")

def modify_collection(request):
    if request.method == 'POST':
        data = {
            'user_id':request.POST['user_id'],
            'client_id':request.POST['client_id'],
            'anime_name':request.POST['anime_name'],
            'episode_num':request.POST['episode_num'],
            'director':request.POST['director'],
            'collection_type':request.POST['collection_type'],
            'rating':request.POST['rating'],
            'comment':request.POST['comment'],
        }
        if usr_check(data['user_id'],data['client_id']):
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
            return HttpResponse("用户认证失败，是不是没有登录？")
    else:
        return HttpResponse("请使用POST方法")

def delete_collection(request):
    if request.method == 'GET':
        data = {
            'user_id':request.GET['user_id'],
            'client_id':request.GET['client_id'],
            'anime_name':request.GET['anime_name'],
        }
        if usr_check(data['user_id'],data['client_id']):
            res = AnimeCollectionData.objects.filter(user_id=data['user_id'],anime_name=data['anime_name']).first()
            if res:
                res.delete()
                return HttpResponse("删除成功")
            else:
                return HttpResponse("您并没有收藏这部番剧")
        else:
            return HttpResponse("用户认证失败，是不是没有登录？") 
    else:
        return HttpResponse("请使用GET方法")
    
def search_collection(request):
    '''context字典中返回一个result列表，其中元素为有anime_name和url的字典'''
    if request.method == 'GET':
        data = {
            'user_id':request.GET['user_id'],
            'client_id':request.GET['client_id'],
            'anime_name':request.GET['anime_name'],
        }
        if usr_check(data['user_id'],data['client_id']):
            res = AnimeCollectionData.objects.filter(user_id=data['user_id'],anime_name__iregex='.*'+data['anime_name']+'.*').first()
            if res:
                #详情页url
                url = 'http://localhost:8000/anime/collection_data/s?user_id='+res.user_id+'&anime_name='+res.anime_name+'&client_id='+data['client_id']
                result = []
                result.append({
                    'anime_name':res.anime_name,
                    'url':url,
                })
                context = {
                    'result':result
                }
                return HttpResponse(str(context))
            else:
                return HttpResponse("搜索无结果")
        else:
            return HttpResponse("用户认证失败，是不是没有登录？") 
    else:
        return HttpResponse("请使用GET方法")
    
def view_collections(request):
    '''context字典中返回一个result列表，其中元素为有anime_name和url的字典'''
    if request.method == 'GET':
        data = {
            'user_id':request.GET['user_id'],
            'client_id':request.GET['client_id'],
        }
        if usr_check(data['user_id'],data['client_id']):
            res = AnimeCollectionData.objects.filter(user_id=data['user_id'])
            result = []
            for i in res:
                tmp = {
                    'anime_name':i.anime_name,
                    #详情页url
                    'url':'http://localhost:8000/anime/collection_data/s?user_id='+i.user_id+'&anime_name='+i.anime_name+'&client_id='+data['client_id']
                }
                result.append(tmp)
            context={
                'result':result
            }
            return HttpResponse(str(context))
    #        return render(request,'all_collections.html',context=context)#后续做个网页链接的生成
        else:
            return HttpResponse("用户认证失败，是不是没有登录？") 
    else:
        return HttpResponse("请使用GET方法")

def collection_data(request):
    '''返回一个context字典，内含有番剧的数据'''
    if request.method == 'GET':
        data = {
            'user_id':request.GET['user_id'],
            'client_id':request.GET['client_id'],
            'anime_name':request.GET['anime_name'],
        }
        if usr_check(data['user_id'],data['client_id']):
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
            return HttpResponse("用户认证失败，是不是没有登录？")
    else:
        return HttpResponse("请使用GET方法")
