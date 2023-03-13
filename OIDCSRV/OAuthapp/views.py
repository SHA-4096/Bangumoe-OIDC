from django.shortcuts import render,HttpResponse,redirect
import jwt
import time
from OAuthapp.models import OAuthTable

# Create your views here.

exp_time = 1000000
#---------------------------#
def generate_token(uid,name,exp,client_secret):
    payload = {
        'user_id': uid,
        'username': name,
        'exp': int(time.time())+exp_time  # 过期时间，以Unix时间戳表示
    }

    secret_key = client_secret
    access_token = jwt.encode(payload, secret_key, algorithm='HS256')

def usr_auth(sitename):
    '''应该要做一个网页的，先留个锅'''
    t = input('是否授权来自'+sitename+"的请求？y/n")
    if(t == 'y'):
        return True
    else:
        return False

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
