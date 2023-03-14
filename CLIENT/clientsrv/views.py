from django.shortcuts import render,HttpResponse,redirect
import jwt
import random
import time
# Create your views here.

def rand_gen():
    return str(random.randint(100000000000,10000000000000))+str(time.time())

def auth_success(request):
    if request.method == 'POST':
        return HttpResponse("使用GET方法")
    else:
        #HttpResponse("授权成功,正在发送auth_code/="+request.GET['auth_code'])
        client_secret = str(random)
        payload = {
            'auth_code':request.GET['auth_code'],
            'redirection_url':'http://localhost:8080/token_get_success/s',
            'client_id':'111222',
        }
        client_secret = rand_gen()
        code = jwt.encode(payload,client_secret,algorithm = 'HS256')
        url = 'http://localhost:8000/access_token_request/s?code='+code+"&client_secret="+client_secret
        return redirect(url)

def send_auth_request(request):
    if request.method == 'POST':
        return HttpResponse("使用GET方法")
    else:
        payload = {
            'sitename':request.GET['sitename'],
            'client_id':request.GET['client_id'],
            'state':request.GET['state'],
            'client_secret':request.GET['client_secret'],#这个是没用的，以后删掉
            'redirection_url':'http://localhost:8080/redir_auth/s',
        }
        client_secret = rand_gen()
        code = jwt.encode(payload,client_secret,algorithm = 'HS256')
        return redirect('http://localhost:8000/auth2/s?code='+str(code)+'&client_secret='+str(client_secret))#向服务器传code和secret，用hs256加密
    
def token_get_success(request):
    if request.method == 'GET':
        return HttpResponse("Token="+request.GET['access_token'])
    else:
        HttpResponse("使用GET方法")
        
def ID_token_request(request):
    '''传入access_token,client_id'''
    if request.method == 'GET':
        access_token = request.GET['access_token']
        client_id = request.GET['client_id']
        client_secret = rand_gen()
        payload = {
            'access_token':access_token,
            'client_id':client_id,
            'redirection_url':'http://localhost:8080/ID_token_responded/s'
        }
        code = jwt.encode(payload,client_secret,algorithm='HS256')
        url = 'http://localhost:8000/query_with_access_token/s?code='+code+'&client_secret='+client_secret+''
        return redirect(url)
def ID_token_responded(request):
    '''处理id_token请求后的响应'''
    return HttpResponse(request.GET['status'])
    