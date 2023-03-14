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
    secret_key = str(random.randint(10000000,1000000000))+str(time.time())
    print(res.client_id)
    access_token = jwt.encode(payload, secret_key, algorithm='HS256')
    if res:
        res.access_token_key = secret_key#后期填坑：存不进去||已解决：在主函数里面先进行一次查询操作
        res.save()
        print(res.access_token_key)
    else:
        return 'Failed'
    return access_token

def decode_access_token(token,secret_key):
    '''对access_token解密，返回一个payload列表'''
    payload = jwt.decode(token,secret_key,algorithms=['HS256'])
    return payload

def usr_auth(table):
    '''应该要做一个网页的，先留个锅;传入的是一个列表,成功的话返回authcode,否则直接提示授权失败'''
    HttpResponse("正在授权")
    t = input('是否授权来自'+table['sitename']+"的请求？y/n")
    if(t == 'y'):
        usr_name= input("用户名")
        passwd = passwrd_encode(input("密码"))
        res = UserInfo.objects.filter(name = usr_name,password = passwd).first()
        authcode_to_return = generate_auth_code()
        if res:
            res_chk = OAuthTable.objects.filter(client_id=table['client_id']).first()
            if res_chk:#已经请求过了就直接更新
                res_chk.authed_uid=usr_name
                res_chk.auth_code=authcode_to_return
                res_chk.auth_code_expired='False'
                res_chk.save()
            else:
                tmp = OAuthTable(sitename=table['sitename'],client_id=table['client_id'],client_secret=table['client_secret'],authed_uid = usr_name,auth_code = authcode_to_return,auth_code_expired = 'False',access_token_key = '123456')
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
            res = OAuthTable.objects.filter(auth_code=code_content['auth_code'],auth_code_expired='False').first()#再次查询更新数据，否则access_token_key会变成空值
            if access_token == 'Failed':
                return HttpResponse("Token未能正确生成")
            res.auth_code_expired='True'
            res.save()
            url = code_content['redirection_url']+'?access_token='+access_token
            return redirect(url)
        else:#数据库中没有这个auth_code
            return HttpResponse("这个请求非法，因为用户并未授权此client")
        
def query_with_access_token(request):
    '''用户传入hs256加密的code内含client_id,access_token,redirection_url,还传入client_secret'''
    if request.method == 'GET':
        code = request.GET['code']
        client_secret = request.GET['client_secret']
        code_content = jwt.decode(code,client_secret,algorithms=['HS256'])
        access_token = code_content['access_token']
        client_id = code_content['client_id']
        redirection_url = code_content['redirection_url']
        res = OAuthTable.objects.filter(client_id=client_id).first()
        if res:
            decoded_token = decode_access_token(access_token,res.access_token_key)
            if decoded_token['client_id'] == client_id:#验证token的真实性
                #decode失败会得到exception（未处理）
                url = redirection_url
                return redirect(url,method = 'GET')
            else:
                return HttpResponse("这个access token似乎不是这个client申请的")
        else:
            return HttpResponse("该client未被授权")
        
    else:
        return HttpResponse("使用GET方法")
    