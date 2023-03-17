from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
#from django.forms import MyForm
from mainsrv.models import UserInfo
import hashlib
import time


max_regtime = 300

#-------------------------------------#



def encode_md5(s):
    m = hashlib.md5()
    m.update(s.encode(encoding='utf-8'))
    res = m.hexdigest()
    return res


def password_encode(s):
    '''密码存储的加密'''
    return encode_md5(s)


def send_code(s,email):
    #以后再接入API
    print(s)

def checkusr(usr,state):
    '''用于删除长时间不认证的用户，以及控制用户发邮件的频率'''
    if state == 1:#登录
        nowtime = time.time()
        if nowtime - float(usr.reg_time) > max_regtime and usr.usrverified == 'False':
            usr.delete()
    elif state == 2:
        pass#等待填坑
    else:
        pass
        
    

#---------------------------------------#


def usrlogin(request):
    if(request.method == 'POST'):
        name = request.POST['name']
        password = request.POST['password']
        client_id = request.POST['client_id']
        res = UserInfo.objects.filter(name=name,password=password_encode(password)).first()
        if(res):
            if res.usrverified == 'True':#用户已经完成认证
                res.is_online = 'True'
                res.online_client_id = client_id
                res.save()#保存登录状态
                txt = "欢迎"+str(request.POST['name'])+'<br>你的信息如下：'+"<br>邮箱"+res.email+"<br>头像<img src="+res.image+' alt=（头像似乎走丢了）>'+"<br>个人简介"+res.profile            
                return HttpResponse(txt)
            else:
                checkusr(res,1)#如果验证码过期了就删掉数据库对应数据
                return HttpResponse("用户名或密码错误！")
        else:
            return HttpResponse("用户名或密码错误！")
    else:
        return HttpResponse("使用POST方法")
    

def usrlogout(request):
    if request.method == 'POST':
        data = {
            'name':request.POST['name'],
            'client_id':request.POST['client_id'],
        }
        res = UserInfo.objects.filter(name=data['name'],online_client_id=data['client_id'],is_online='True').first()
        if res:#用户确实登入了
            res.is_online = 'False',
            res.online_client_id = str(time.time()),
            res.save()
            return HttpResponse("登出成功")
        else:
            return HttpResponse("这个请求非法，可能是已经登出或者没有登录")
    else:
        return HttpResponse("使用POST方法")
    

def usrregister(request):
    if(request.method == 'POST'):
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        nickname = request.POST['nickname']
        profile = request.POST['profile']
        image = request.POST['image']
        res = UserInfo.objects.filter(name=name)
        if(res):
            return HttpResponse("和现有用户重名了！")
        else:
            tmp = UserInfo(name = name,password = password_encode(password),email=email,nickname=nickname,profile=profile,image=image,usrverified="False",reg_time=time.time())
            lnk = 'http://localhost:8000/register-verify/s?code='+encode_md5(name)+encode_md5(nickname)+'&name='+name+"\n请在"+str(int(max_regtime/60))+"min内完成认证"
            send_code(lnk,email)
            tmp.save()
            return HttpResponse("请去邮箱查收邮件，点击链接之后便可以完成注册"+"\n请在"+str(int(max_regtime/60))+"min内完成认证")
    else:
        return HttpResponse("还不会写HTML呢！可以先用client.py跑一下哦！")
    
def verify(request):
    if request.method == 'POST':
        return HttpResponse("请使用GET方法访问")
    else:
        reg_code = request.GET['code']
        name = request.GET['name']
        res = UserInfo.objects.filter(name=name).first()
        if res:
            if reg_code == encode_md5(name)+encode_md5(res.nickname):
                res.usrverified = "True"
                res.save()
                return HttpResponse("注册成功！")
            else:
                return HttpResponse("这个链接无效！")
        else:
            return HttpResponse("这个链接无效！")

def check_online_state(request):
    '''GET方法，验证这个client是否登入了相应的用户，传入client_id和name，返回一个Httpresponse，其为True或False(字符串)'''
    if request.method == 'GET':
        data = {
            'name':request.GET['name'],
            'client_id':request.GET['client_id'],
        }
        res = UserInfo.objects.filter(name=data['name'],online_client_id=data['client_id'],is_online='True').first()
        if res:
            return HttpResponse('True')
        else:
            return HttpResponse('False')
    else:
        return HttpResponse("请使用GET方法访问")