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
        res = UserInfo.objects.filter(name=name,password=password).first()
        if(res):
            if res.usrverified == 'True':
                txt = "欢迎"+str(request.POST['name'])+'\n你的信息如下：'+"\n邮箱"+res.email+"\n头像链接"+res.image+"\n个人简介"+res.profile            
                return HttpResponse(txt)
            else:
                checkusr(res,1)
                return HttpResponse("用户名或密码错误！")
        else:
            return HttpResponse("用户名或密码错误！")
    else:
        return HttpResponse("还不会写HTML呢！可以先用client.py跑一下哦！")
    
    
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
            tmp = UserInfo(name = name,password = password,email=email,nickname=nickname,profile=profile,image=image,usrverified="False",reg_time=time.time())
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