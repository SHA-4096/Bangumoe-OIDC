from django.shortcuts import render,HttpResponse,redirect
import jwt
import random
import time
# Create your views here.

state_tmp = None#用来存储state
def state_gen():
        payload_state = {
            'rand':rand_gen()+'csbcnkauhckwajeck',
        }
        state = jwt.encode(payload_state,rand_gen(),algorithm='HS256')#随机生成state参数
        return state

def rand_gen():
    return str(random.randint(100000000000,10000000000000))+str(time.time())

def auth_success(request):
    '''成功获得授权码'''
    global state_tmp
    if request.method == 'POST':
        return HttpResponse("使用GET方法")
    else:
        #HttpResponse("授权成功,正在发送auth_code/="+request.GET['auth_code'])
        client_id = '111222'#------------------------先给个定值方便调试
        state = state_gen()
        state_tmp = state
        auth_code=request.GET['auth_code']
#==========================在这里可以修改scopes====================================
        redirection_url='http://localhost:8080/'
#        code = jwt.encode(payload,client_secret,algorithm = 'HS256')
        url = 'http://localhost:8000/access_token_request/s?'+'state='+state+'&client_id='+client_id+'&redirection_url='+redirection_url+'&auth_code='+auth_code+'&scopes=openid%20profile'
        return redirect(url,permanent=True)

def send_auth_request(request):
    '''请求一个auth_code'''
    global state_tmp
    if request.method == 'POST':
        return HttpResponse("使用GET方法")
    else:
        payload = {
            'sitename':request.GET['sitename'],
            'client_secret':request.GET['client_secret'],#这个是没用的，以后删掉
        }
        state = state_gen()
        state_tmp = state
        client_secret = rand_gen()
        redirection_url='http://localhost:8080/'
        client_id = request.GET['client_id']
        sitename = request.GET['sitename']
        client_secret=rand_gen()
#===========================这里修改response_type=========================
        url = 'http://localhost:8000/auth2/s?client_secret='+str(client_secret)+'&response_type='+'code'+'&redirection_url='+redirection_url+'&client_id='+client_id+'&sitename='+sitename+'&client_secret='+client_secret
        return redirect(url+"&state="+state,permanent=True)#向服务器传code和secret，用hs256加密
    
def token_get_success(request):
    '''拿到access_token,refresh_token,ID_token\ID_token_key和iss'''
    global state_tmp
    if request.method == 'GET':
        #先检查state
        if request.GET['state'] != state_tmp:
            return HttpResponse("state不匹配，可能是csrf攻击")
        else:
            decoded_ID_token = None
            if request.GET['ID_token'] == 'None':
                pass
            else:
                decoded_ID_token = jwt.decode(request.GET['ID_token'],request.GET['ID_token_key'],algorithms=['HS256'])
            return HttpResponse("access_token="+request.GET['access_token']+'\nrefresh_token='+request.GET['refresh_token']+'\nID_token='+request.GET['ID_token']+'\nID_token_key='+request.GET['ID_token_key']+'\niss='+request.GET['iss']+'\nDecoded_ID_token='+str(decoded_ID_token))
    else:
        HttpResponse("使用GET方法")
        
def ID_token_request(request):
    '''传入access_token,client_id'''
    global state_tmp
    if request.method == 'GET':
        access_token = request.GET['access_token']
        client_id = request.GET['client_id']
        client_secret = rand_gen()
        payload = {
            'access_token':access_token,
            'client_id':client_id,
            'redirection_url':'http://localhost:8080/'
        }
        code = jwt.encode(payload,client_secret,algorithm='HS256')
        state_tmp = state_gen()
        url = 'http://localhost:8000/query_with_access_token/s?code='+code+'&client_secret='+client_secret+'&state='+state_tmp
        return redirect(url,permanent=True)

def ID_token_responded(request):
    global state_tmp
    '''处理id_token请求后的响应'''
    if request.GET['state'] != state_tmp:
        return HttpResponse("state不匹配，可能是csrf攻击")
    else:
        return HttpResponse(request.GET['status'])

def refresh_access_token(request):
    global state_tmp
    if request.method == 'GET':
        '''传入client_id,refresh_token'''
        redirection_url = 'http://localhost:8080/'
        client_id = request.GET['client_id']
        refresh_token = request.GET['refresh_token']
        client_secret = rand_gen()
        payload = {
            'client_id':client_id,
        }
        code = jwt.encode(payload,client_secret,algorithm='HS256')
        state_tmp = state_gen()
        url = 'http://localhost:8000/renew_access_token/s?code='+code+'&redirection_url='+redirection_url+'&refresh_token='+refresh_token+'&client_secret='+client_secret+'&state='+state_tmp
        return redirect(url+'&state='+state_tmp,method='GET',permanent=True)
    else:
        return HttpResponse("Use GET")
def access_token_refreshed(request):
    '''已经废弃'''
    global state_tmp
    if request.method == 'GET':
        if request.GET['state'] != state_tmp:
            return HttpResponse("state不匹配，可能是csrf攻击")
        else:
            return HttpResponse("New access_token:"+request.GET['access_token'])
    else:
        return HttpResponse("Use GET")