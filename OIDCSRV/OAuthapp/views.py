from django.shortcuts import render,HttpResponse,redirect
import jwt
import time
from OAuthapp.models import OAuthTable
from mainsrv.models import UserInfo
import random
# Create your views here.

exp_time = 1000000
#---------------------------#

def passwrd_encode(s):
    '''填坑：密码存储的加密'''
    return s

def generate_token(uid,client_id):
    '''token中存储的client_id将会被当作后续验证的手段,user_id是授权用户的id,对client不可见;要事先验证uid的有效性,access_token_key存入数据库'''
    payload = {
        'user_id': uid,
        'client_id':client_id,
        'exp': int(time.time())+exp_time  # 过期时间，以Unix时间戳表示
    }
    res = OAuthTable.objects.filter(client_id = client_id).first()
    secret_key = '123456'#str(random.randint(10000000000,1000000000000))+str(time.time())
    access_token = jwt.encode(payload, secret_key, algorithm='HS256')
    if res:
        res.access_token_key = secret_key
        res.save()
    else:
        return 'Failed'
    return access_token

def decode_token(token,secret_key):
    '''对access_token解密，返回一个payload列表'''
    payload = jwt.decode(token,secret_key,algorithms=['HS256'])

def usr_auth(table):
    '''应该要做一个网页的，先留个锅;传入的是一个列表,成功的话返回authcode,否则直接提示授权失败'''
    HttpResponse("正在授权")
    t = input('是否授权来自'+table['sitename']+"的请求？y/n")
    if(t == 'y'):
        usr_name= input("用户名")
        passwd = passwrd_encode(input("密码"))
        res = UserInfo.objects.filter(name = usr_name,password = passwd).first()
        if res:
            authcode_to_return = generate_auth_code()
            tmp = OAuthTable(sitename=table['sitename'],client_id=table['client_id'],client_secret=table['client_secret'],authed_uid = usr_name,auth_code = authcode_to_return,auth_code_expired = 'False')
            tmp.save()
            url = table['redirection_url']+"?auth_code="+authcode_to_return
            return url
        else:
            return 'Failed'
    else:
        return "Failed"


def generate_auth_code():
    '''返回一串随机的字符串'''
    return str(random.randint(10000000000000000000,10000000000000000000000))+str(time.time())
#----------------------------#

def get_clientrequest(request):
    if request.method == 'POST':
        return HttpResponse("请使用GET方法")
    else:
        sitename = request.GET['sitename']
        client_id = request.GET['client_id']
        state = request.GET['state']
        client_secret = request.GET['client_secret']
        redirection_url = request.GET['redirection_url']
        tmp = OAuthTable(client_id=client_id,client_secret=client_secret,redirection_url=redirection_url,sitename=sitename)
        tmp.save()
        return redirect('http://localhost:8000/auth/s?client_id='+client_id+'&sitename='+sitename,method = 'GET')

def user_authenticate(request):
    if request.method == 'POST':
        return HttpResponse("请使用GET方法")
    else:
        client_id = request.GET['client_id']
        sitename = request.GET['sitename']
        auth_res = usr_auth(sitename)
        if auth_res:
            res = OAuthTable.objects.filter(client_id=client_id).first()
            return redirect(res.redirection_url,method = 'GET')
        else:
            return HttpResponse('授权失败！')

def user_authenticate2(request):
    '''读入code,client_secret,返回auth_code'''
    if request.method == 'POST':
        return HttpResponse("请使用GET方法")
    else:
        code = request.GET['code']
        client_secret = request.GET['client_secret']
        res = jwt.decode(code,client_secret,algorithms=['HS256'])      
        client_id = res['client_id']
        sitename = res['sitename']
        redirection_url = res['redirection_url']
        url = usr_auth(res)
        if url == 'Failed':
            return HttpResponse("认证失败")    
        else:
            return redirect(url)
    

def access_token_request(request):
    '''请求access_token:传入HS256加密的code，内含auth_code，redirection_url以及client_id，当然还会传入client_secret,返回一个access_token,以后验证时需要client_id'''
    if request.method == 'POST':
        return HttpResponse("请使用GET方法")
    else:
        code = request.GET['code']
        client_secret = request.GET['client_secret']
        code_content = jwt.decode(code,client_secret,algorithms=['HS256'])
        res = OAuthTable.objects.filter(auth_code=code_content['auth_code'],auth_code_expired='False').first()
        if res:
            access_token = generate_token(res.authed_uid,res.client_id)
            if access_token == 'Failed':
                return HttpResponse("Token未能正确生成")
            res.auth_code_expired='True'
            res.save()
            url = code_content['redirection_url']+'?access_token='+access_token
            return redirect(url)
        else:#数据库中没有这个client_id
            return HttpResponse("这个请求非法，因为用户并未授权此client")