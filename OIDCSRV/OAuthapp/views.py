from django.shortcuts import render,HttpResponse,redirect
import jwt
import time
from OAuthapp.models import OAuthTable
from mainsrv.models import UserInfo
import random
import re
import json
import hashlib
# Create your views here.

exp_time = 3600#过期时间
#---------------------------#

def encode_md5(s):
    m = hashlib.md5()
    m.update(s.encode(encoding='utf-8'))
    res = m.hexdigest()
    return res


def password_encode(s):
    '''密码存储的加密'''
    return encode_md5(s)

def randgen():
    return str(random.randint(10000000,1000000000))+str(time.time())

def generate_access_token(uid,client_id):
    '''access_token中存储的client_id将会被当作后续验证的手段,user_id是授权用户的id,对client不可见;要事先验证uid的有效性,access_token_key存入数据库'''
    payload = {
        'user_id': uid,
        'client_id':client_id,
        'expire': int(time.time())+exp_time  # 过期时间，以Unix时间戳表示
    }
    res = OAuthTable.objects.filter(client_id = client_id).first()
    secret_key = str(random.randint(10000000,1000000000))+str(time.time())#以后重构一下
    access_token = jwt.encode(payload, secret_key, algorithm='HS256')
    if res:
        res.access_token_key = secret_key#后期填坑：存不进去||已解决：在主函数里面先进行一次查询操作
        res.save()
#        print(res.access_token_key)
    else:
        return 'Failed'
    return access_token

def generate_refresh_token(uid,client_id):
    '''与access_token一样要验证client_id'''
    payload = {
        'user_id': uid,
        'client_id':client_id,
    }
    res = OAuthTable.objects.filter(client_id = client_id).first()
    secret_key = randgen()
    refresh_token = jwt.encode(payload, secret_key, algorithm='HS256')
    if res:
        res.refresh_token_key = secret_key#后期填坑：存不进去||已解决：在主函数里面先进行一次查询操作
        res.save()
#        print(res.access_token_key)
    else:
        return 'Failed'
    return refresh_token

def generate_ID_token(uid,client_id,scopes):
    '''生成ID_token，返回字段为token和key的字典'''
    res = UserInfo.objects.filter(name=uid).first()
    email = ' '
    profile = ' '
    if not re.findall(pattern='openid',string=scopes):
        dat = {
            'token':'None',
            'key':'None',
        }
        return dat
    if re.findall(pattern='email',string=scopes):
        email = res.email
    if re.findall(pattern='profile',string=scopes):
        profile = res.profile
    payload = {
        'iss':'http://localhost:8000/',
        'sub':uid,
        'aud_id':client_id,#避免框架直接抛出exception就不叫aud了，expire同
        'expire':time.time()+exp_time,
        'iat':time.time(),
        'email':email,
        'profile':profile,
    }
    ID_token_key = randgen()
    ID_token = jwt.encode(payload,ID_token_key,algorithm='HS256')
    dat = {
        'token':ID_token,
        'key':ID_token_key,
    }
    return dat



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
        passwd = str(input("密码"))
        res = UserInfo.objects.filter(name = usr_name,password = password_encode(passwd)).first()
        authcode_to_return = generate_auth_code()
        if res:
            res_chk = OAuthTable.objects.filter(client_id=table['client_id']).first()
            if res_chk:#已经请求过了就直接更新
                res_chk.authed_uid=usr_name
                res_chk.auth_code=authcode_to_return
                res_chk.auth_code_expired='False'
                res_chk.redirection_url=table['redirection_url']
                res_chk.save()
            else:
                tmp = OAuthTable(sitename=table['sitename'],client_id=table['client_id'],client_secret=table['client_secret'],authed_uid = usr_name,auth_code = authcode_to_return,auth_code_expired = 'False',access_token_key = '123456',redirection_url=table['redirection_url'])
                tmp.save()
            url = table['redirection_url']+"redir_auth/s?auth_code="+authcode_to_return
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
        url = redirection_url+'auth2/s?client_id='+client_id+'&sitename='+sitename
        return redirect(url+'&state='+request.GET['state'],method = 'GET',permanent=True)

def user_authenticate(request):
    if request.method == 'POST':
        return HttpResponse("请使用GET方法")
    else:
        client_id = request.GET['client_id']
        sitename = request.GET['sitename']
        table = {
            'client_id':client_id,
            'sitename':sitename,
            'redirection_url':request.GET['redirection_url']
        }
        auth_res = usr_auth(table)
        if auth_res:
            res = OAuthTable.objects.filter(client_id=client_id).first()
            red = redirect(res.redirection_url+'&state='+request.GET['state'],method = 'GET',permanent=True)
            red.status_code = 404
            return red
        else:
            return HttpResponse('授权失败！')

def user_authenticate2(request):
    '''返回auth_code'''
    if request.method == 'POST':
        return HttpResponse("请使用GET方法")
    else:
        if request.GET['response_type'] == 'code':
            res = {
                'client_id':request.GET['client_id'],
                'sitename':request.GET['sitename'],
                'redirection_url':request.GET['redirection_url'],
                'sitename':request.GET['sitename'],
                'client_secret':request.GET['client_secret'],
            }
            url = usr_auth(res)
            if url == 'Failed':
                return HttpResponse("认证失败")    
            else:
                return redirect(url+'&state='+request.GET['state'],permanent=True)
        else:
            return HttpResponse('目前只支持code授权方式请求')
    

def access_token_request(request):
    '''请求access_token:auth_code，redirection_url以及client_id，scopes，返回access_token、ID_token、ID_token_key,iss和refresh_token,以后验证时需要client_id'''
    if request.method == 'POST':
        return HttpResponse("请使用GET方法")
    else:
        res = OAuthTable.objects.filter(auth_code=request.GET['auth_code'],auth_code_expired='False',redirection_url=request.GET['redirection_url']).first()
        scopes = request.GET['scopes']
        if res:#已经确认auth_code的合法性(检查了重定向url的真实性)
            access_token = generate_access_token(res.authed_uid,res.client_id)
            refresh_token = generate_refresh_token(res.authed_uid,res.client_id)
            ID_token_tmp = generate_ID_token(res.authed_uid,res.client_id,scopes)
            iss = 'http://localhost:8000/'
            #再次查询更新数据，否则access_token_key会变成空值
            res = OAuthTable.objects.filter(auth_code=request.GET['auth_code'],auth_code_expired='False').first()
            if access_token == 'Failed':
                return HttpResponse("Token未能正确生成")
            res.auth_code_expired='True'
            res.save()
            url = request.GET['redirection_url']+'token_get_success/s'+'?access_token='+access_token+'&refresh_token='+refresh_token+'&ID_token='+ID_token_tmp['token']+'&ID_token_key='+ID_token_tmp['key']+'&iss='+iss
            return redirect(url+'&state='+request.GET['state'],permanent=True)
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
            decoded_access_token = decode_access_token(access_token,res.access_token_key)
            if decoded_access_token['client_id'] == client_id:#验证token的真实性
                if time.time()>decoded_access_token['expire']:#decode失败会得到exception（未处理）
                    url = redirection_url+'ID_token_responded/s'+'?status=Invalid_token_error_expired'
                    return redirect(url+'&state='+request.GET['state'],method = 'GET',permanent=True)
                else:
                    url = redirection_url+'ID_token_responded/s'+'?status=success'
                    return redirect(url+'&state='+request.GET['state'],method = 'GET',permanent=True)
            else:
                return HttpResponse("这个access token似乎不是这个client申请的")
        else:
            return HttpResponse("该client未被授权")
    else:
        return HttpResponse("使用GET方法")

def renew_access_token(request):
    '''传入HS256加密的code[client_id],以及client_secret,refresh_token,返回access_token、ID_token、ID_token_key,iss以及原本的refresh_token'''
    if request.method == 'GET':
        decoded_code = jwt.decode(request.GET['code'],request.GET['client_secret'],algorithms=['HS256'])
        client_id = decoded_code['client_id']
        refresh_token = request.GET['refresh_token']
        res = OAuthTable.objects.filter(client_id=client_id).first()
        if res:
            token_key = res.refresh_token_key
            decoded_token = jwt.decode(refresh_token,token_key,algorithms=['HS256'])
            if decoded_token['client_id'] == client_id:#确认token有效
                access_token = generate_access_token(decoded_token['user_id'],decoded_token['client_id'])
                refresh_token = generate_refresh_token(res.authed_uid,res.client_id)
                ID_token_tmp = generate_ID_token(res.authed_uid,res.client_id)
                iss = 'http://localhost:8000/'
                url = request.GET['redirection_url']+'token_get_success/s'+'?access_token='+access_token+'&refresh_token='+refresh_token+'&ID_token='+ID_token_tmp['token']+'&ID_token_key='+ID_token_tmp['key']+'iss='+iss
                return redirect(url+'&state='+request.GET['state'],method = 'GET',permanent=True)
            else:
                return HttpResponse("这个refresh_token无效")
        else:
            return HttpResponse('token无效：找不到对应的client_id')
    else:
        return HttpResponse("使用GET方法")


def doc_show(request):
    global doc_data
    return HttpResponse(json.dumps(doc_data))

#=======================以下是对接口的说明===================
doc_data = {
 "issuer": "http://localhost:8000/",
 "authorization_endpoint": "http://localhost:8000/auth2/s",
 "token_endpoint": "http://localhost:8000/access_token_request/s",
 "userinfo_endpoint": "http://localhost:8000/query_with_access_token/s",
 "refresh_token_endpoint":"http://localhost:8000/renew_access_token/s",
 "response_types_supported": [
  "code",
 ],
 "id_token_signing_alg_values_supported": [
  "RS256"
 ],
 "scopes_supported": [
  "openid",
  "email",
  "profile"
 ],
 "claims_supported": [
  "暂时没有做access_token请求数据的功能"
 ],
 "grant_types_supported": [
  "authorization_code",
  "refresh_token",
 ]
}
