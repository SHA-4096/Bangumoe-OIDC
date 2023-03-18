from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpRequest
import random
import jwt
from . import sensitive
import time
import requests
import json
import urllib3
import re
# Create your views here.
state_global = 111
header_global = {'User-Agent':'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)',
                 'Authorization':'Bearer '}
client_id = sensitive.get_client_id() 
client_secret = sensitive.get_client_secret()

user_id_bangumoe = '11111'
client_id_bangumoe = '111222'

apiname = 'https://api.bgm.tv/'
tokens = {
    'access_token':'none',
    'refresh_token':'none',
    'expires_in':1,
    'scope':'none',
    'user_id':'776529',
}

#一些工具方法

def rand_gen():
    return str(random.randint(100000000000,10000000000000))+str(time.time())

def get_details(subject_id):
    params = {
        'subject_id':subject_id,
    }
    url = 'https://api.bgm.tv/user/776529/progress'
    http = urllib3.PoolManager()
    r = http.request('GET',url=url,headers=header_global,fields=params)
    res = json.loads(r.data.decode('utf-8'))
#    sync_collection_detail(res['eps'])
    return

def state_gen():
        payload_state = {
            'rand':rand_gen()+'csbcnkauhckwajeck',
        }
        state = jwt.encode(payload_state,rand_gen(),algorithm='HS256')#随机生成state参数
        return state

def sync_collection(list):
    for i in list:
        url = 'http://localhost:8000/anime/collect_anime/s'
        data = {
            'user_id':user_id_bangumoe,
            'client_id':client_id_bangumoe,
            'anime_name':i['subject']['name'],
            'episode_num':i['subject']['eps'],
            'director':'not_supported_yet',#i['subject']['director'],
            'collection_type':i['subject']['type'],
            'rating':'not_supported_yet',#i['subject']['rating'],
            'comment':'not_supported_yet',#i['subject']['rating'],
        }
        anime_url = i['subject']['url']
        res = requests.post(url,data=data).text
        print(res)
        if res == '收藏成功':
            text = '你的好友'+data['user_id']+'收藏了<a href='+anime_url+' >'+data['anime_name']+'这部剧</a>'
            send_data(text)
    return

def send_data(content):
    '''发送信息给所有好友'''
    data = {
        'user_id':user_id_bangumoe,
        'client_id':client_id_bangumoe,
        'content':content,
    }
    url = 'http://localhost:8000/anime/send_dataflow/'
    http = urllib3.PoolManager()
    r = http.request('POST',url=url,fields=data)
    res = r.data.decode('utf-8')
    print(res)
    return
    

#授权相关

def refresh_access_token(request):
    state_global = state_gen()
    param = {
        'grant_type':'refresh_token',
        'client_id':client_id,
        'client_secret':client_secret,
        'refresh_token':tokens['refresh_token'],
        'redirect_uri':'http://localhost:8100/auth/callback/s',
    }
    url = 'https://bgm.tv/oauth/access_token'
    http = urllib3.PoolManager()
    r = http.request('POST',url=url,fields=param)
    res = dict(json.loads(r.data.decode('utf-8')))
    tokens['access_token'] = res['access_token']
    tokens['refresh_token'] = res['refresh_token']
    tokens['expires_in'] = res['expires_in']
    tokens['scope'] = res['scope']
    tokens['user_id'] = res['user_id']
    header_global['Authorization'] = 'Bearer '+tokens['access_token']
    return HttpResponse(str(r.data.decode('utf-8'))+'<br><a href=http://localhost:8100/mainpage/>回到主页</a>')

#        text+=i['subject']['name']+' '+i['subject']['url']+' '+str(i['subject']['id'])+ ' 集数：'+str(i['subject']['eps'])+'<br>'
#---------------------------------------------------------

def sync_collection_detail(list,name):
    for i in list:
        url = 'http://localhost:8000/anime/collect_anime_detail_sync/s'
        data = {
            'user_id':user_id_bangumoe,
            'client_id':client_id_bangumoe,
            'anime_name':name,
            'episode_num':i['eps'],
            'director':'not_supported_yet',#i['subject']['director'],
            'collection_type':i['status']['cn_name'],
            'rating':'not_supported_yet',#i['subject']['rating'],
            'comment':'not_supported_yet',#i['subject']['rating'],
        }
        print(requests.post(url,data=data).text)

def auth_callback(request):
    global state_global
    if request.method == 'GET':
        if state_global != request.GET['state']:
            return HttpResponse("state不匹配")
        code = request.GET['code']
        print(code)
        param = {
            'grant_type':'authorization_code',
            'client_id':client_id,
            'client_secret':client_secret,
            'code':code,
            'redirect_uri':'http://localhost:8100/auth/callback/s',
        }
        url = "https://bgm.tv/oauth/access_token"
        url1 = "https://bgm.tv/oauth/access_token"+'?grant_type='+'authorization_code'+'&client_id='+client_id+'&client_secret='+client_secret+'&code='+code+'&redirect_uri='+'http://localhost:8100/auth/callback/s'+'&state='+state_global
        http = urllib3.PoolManager()
        state_global = state_gen()
        r = http.request('POST',url,fields=param)
        res = dict(json.loads(r.data.decode('utf-8')))
        tokens['access_token'] = res['access_token']
        tokens['refresh_token'] = res['refresh_token']
        tokens['expires_in'] = res['expires_in']
        tokens['scope'] = res['scope']
        tokens['user_id'] = res['user_id']
        header_global['Authorization'] = 'Bearer '+tokens['access_token']
        return HttpResponse(str(r.data.decode('utf-8'))+'<br><a href=http://localhost:8100/mainpage/>回到主页</a>')
    else:
        return HttpResponse("使用POST方法")

def search(request):
    if request.method == 'GET':
        keyword = request.GET['keyword']
        url =  apiname+'/search/subject/'+keyword
        http = urllib3.PoolManager()
        r = http.request("GET",url,headers=header_global)
        res = json.loads(r.data.decode('utf-8'))
        text = '搜索'+keyword+'的结果如下：<br>'
        for i in res['list']:
            text+='<a href='+i['url']+'>'+i['name']+'</a>'+'<br>'
        return HttpResponse(text)
    else:
        return HttpResponse("使用GET")


def get_collection(request):
    url = 'https://api.bgm.tv/user/'+str(tokens['user_id'])+'/collection?cat=played'
    http = urllib3.PoolManager()
    r = http.request("GET",url,headers=header_global)
#    r1 = re.sub(r'\[|\]', '', r.data.decode('utf-8'))
    res = json.loads(r.data.decode('utf-8'))#exmple:res[0][subject]['name']
    text = '您的数据已经同步至Bangumoe：<br>'
    sync_collection(res)
    for i in res:
        text+='<a href='+i['subject']['url']+'>'+i['subject']['name']+'</a>'+' '+str(i['subject']['id'])+ ' 集数：'+str(i['subject']['eps'])+'<br>'
        get_details(i['subject']['id'])
    return HttpResponse(text)

def bangumoe_view_collection(request):
    if request.method == 'GET':
        data = {
            'user_id':user_id_bangumoe,
            'client_id':client_id_bangumoe,
        }
        url = 'http://localhost:8000/anime/view_collections/s'
        http = urllib3.PoolManager()
        r = http.request('GET',url=url,fields=data)
        res = r.data.decode('utf-8')
        return HttpResponse(res)
    else:
        return HttpResponse("使用GET方法")
def bangumoe_delete_collection(request):
    if request.method == 'GET':
        url = 'http://localhost:8000/anime/delete_collection/s'
        data = {
            'user_id':user_id_bangumoe,
            'client_id':client_id_bangumoe,
            'anime_name':request.GET['anime_name'],
        }
        http = urllib3.PoolManager()
        r = http.request('GET',url=url,fields=data)
        res = r.data.decode('utf-8')
        return HttpResponse(res)
    else:
        return HttpResponse("使用GET方法")
def bangumoe_modify_collection(request):
    if request.method == 'GET':
        url = 'http://localhost:8000/anime/modify_collection/s'
        data = {
                'user_id':user_id_bangumoe,
                'client_id':client_id_bangumoe,
                'anime_name':request.GET['anime_name'],
                'episode_num':request.GET['episode_num'],
                'director':request.GET['director'],
                'collection_type':request.GET['collection_type'],
                'rating':request.GET['rating'],
                'comment':request.GET['comment'],
            }
        http = urllib3.PoolManager()
        r = http.request('POST',url=url,fields=data)
        res = r.data.decode('utf-8')
        return HttpResponse(res)
    else:
        return HttpResponse("使用GET方法")
def bangumoe_add_collection(request):
    if request.method == 'GET':
        url = 'http://localhost:8000/anime/collect_anime/s'
        data = {
                'user_id':user_id_bangumoe,
                'client_id':client_id_bangumoe,
                'anime_name':request.GET['anime_name'],
                'episode_num':request.GET['episode_num'],
                'director':request.GET['director'],
                'collection_type':request.GET['collection_type'],
                'rating':request.GET['rating'],
                'comment':request.GET['comment'],
            }
        http = urllib3.PoolManager()
        r = http.request('POST',url=url,fields=data)
        res = r.data.decode('utf-8')
        if res == '收藏成功':
            text = '你的好友'+data['user_id']+'收藏了'+data['anime_name']+'这部剧'
            send_data(text)
        return HttpResponse(res)
    else:
        return HttpResponse("使用GET方法")
def bangumoe_search_collection(request):
    if request.method == 'GET':
        url = 'http://localhost:8000/anime/search_collection/s'
        if request.method == 'GET':
            data = {
                    'user_id':user_id_bangumoe,
                    'client_id':client_id_bangumoe,
                    'anime_name':request.GET['anime_name'],
                }
            http = urllib3.PoolManager()
            r = http.request('GET',url=url,fields=data)
            res = r.data.decode('utf-8')
            return HttpResponse(res)
    else:
        return HttpResponse("使用GET方法")
def bangumoe_collection_data(request):
    url = 'http://localhost:8000/anime/collection_data/s'
    if request.method == 'GET':
        url = 'http://localhost:8000/anime/modify_collection/s'
        data = {
                'user_id':user_id_bangumoe,
                'client_id':client_id_bangumoe,
                'anime_name':request.GET['anime_name'],
            }
        http = urllib3.PoolManager()
        r = http.request('GET',url=url,fields=data)
        res = r.data.decode('utf-8')
        return HttpResponse(res)
    else:
        return HttpResponse("使用GET方法")

def bangumoe_login(request):
    if request.method == 'POST':
        data = {
            'name':request.POST['name'],
            'password':request.POST['password'],
            'client_id':client_id_bangumoe,
        }
        global user_id_bangumoe
        user_id_bangumoe = data['name']
        url = 'http://localhost:8000/usrlogin/'
        http = urllib3.PoolManager()
        r = http.request('POST',url = url,fields=data)
        res = r.data.decode('utf-8')
        return HttpResponse(res+'<br><a href = http://localhost:8100/mainpage/>回到主页</a>')
    else:
        return HttpResponse("使用POST方法")

def bangumoe_logout(request):
    if request.method == 'GET':
        data = {
            'name':user_id_bangumoe,
            'client_id':client_id_bangumoe,
        }
        url = 'http://localhost:8000/usrlogout/s'
        http = urllib3.PoolManager()
        r = http.request('POST',url = url,fields=data)
        res = r.data.decode('utf-8')
        return HttpResponse(res+'<br><a href = http://localhost:8100/mainpage/>回到主页</a>')
    else:
        return HttpResponse("使用GET方法")

def bangumoe_register(request):
    if request.method == 'POST':
        data = {
            'name':request.POST['name'],
            'password':request.POST['password'],
            'password_confirm':request.POST['password_confirm'],
            'email':request.POST['email'],
            'nickname':request.POST['nickname'],
            'profile':request.POST['profile'],
            'image':request.POST['image'],
        }
        if data['password'] != data['password_confirm']:
            return HttpResponse("两次输入密码不同"+'<br><a href = http://localhost:8100/mainpage/>回到主页</a>')
        http = urllib3.PoolManager()
        url = 'http://localhost:8000/usrregister/'
        r = http.request('POST',url = url,fields=data)
        res = r.data.decode('utf-8')
        return HttpResponse(res+'<br><a href = http://localhost:8100/mainpage/>回到主页</a>')
    else:
        return HttpResponse("使用POST方法")

def bangumoe_modify(request):
    if request.method == 'POST':
        data = {
            'name':request.POST['name'],
            'password':request.POST['password'],
            'password_confirm':request.POST['password_confirm'],
            'email':request.POST['email'],
            'nickname':request.POST['nickname'],
            'profile':request.POST['profile'],
            'image':request.POST['image'],
            'client_id':client_id_bangumoe,
        }
        print(data['password'])
        if data['password'] != data['password_confirm']:
            return HttpResponse("两次输入密码不同"+'<br><a href = http://localhost:8100/mainpage/>回到主页</a>')
        http = urllib3.PoolManager()
        url = 'http://localhost:8000/usrmodify/'
        r = http.request('POST',url = url,fields=data)
        res = r.data.decode('utf-8')
        return HttpResponse(res+'<br><a href = http://localhost:8100/mainpage/>回到主页</a>')
    else:
        return HttpResponse("使用POST方法")


#好友相关
def add_friend(request):
    '''POST,传入friend_id'''
    if request.method == 'POST':
        url = 'http://localhost:8000/anime/add_friend/'
        data = {
            'user_id':user_id_bangumoe,
            'client_id':client_id_bangumoe,
            'friend_id':request.POST['friend_id'],
        }
        http = urllib3.PoolManager()
        r = http.request('POST',url=url,fields=data)
        res = r.data.decode("utf-8")
        return HttpResponse(res)
    else:
        return HttpResponse("使用POST方法")

def check_dataflow(request):
    '''POST'''
    if request.method == 'POST':
        url = 'http://localhost:8000/anime/check_dataflow/'
        data = {
            'user_id':user_id_bangumoe,
            'client_id':client_id_bangumoe,
        }
        http = urllib3.PoolManager()
        r = http.request('POST',url=url,fields=data)
        res = r.data.decode("utf-8")
        return HttpResponse(res)
    else:
        return HttpResponse("使用POST方法")

def mainpage(request):
    return render(request,'mainpage.html')

#---------------------------

def token_callback(request):
    return HttpResponse("111")

def request_auth_code(request):
    global state_global
    state_global = state_gen()
    url = sensitive.get_code_url()
    return redirect(sensitive.get_code_url()+'&state='+state_global)

def dummy(requests):
    return HttpResponse("dummy")