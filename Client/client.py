import requests
from django.middleware import csrf
while True:
    a = None
    print("1：登录；2：创建用户\n请输入")
    opt = input()
    if (opt == '1'):
        name = input("用户名:")
        password = input("密码:")

        url = 'http://localhost:8000/usrlogin/'

        data = {
            'name':name,
            'password':password,
    #        'csrfmiddlewaretoken': csrf.get_token(request),
        }
        a = requests.post(url,data)
    else:
        url = 'http://localhost:8000/usrregister/'
        name = input("用户名:")
        password = str(input("密码:"))
        email = input("电子邮箱：")
        image = input("头像链接：")
        nickname = input("昵称：")
        profile = input("个人简介：")
        data = {
            'name':name,
            'password':password,
            'email':email,
            'image':image,
            'nickname':nickname,
            'profile':profile,
            
    #        'csrfmiddlewaretoken': csrf.get_token(request),
        }
        a = requests.post(url,data)
    print(a.text)
