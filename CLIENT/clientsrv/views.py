from django.shortcuts import render,HttpResponse

# Create your views here.


def auth_success(request):
    return HttpResponse("授权成功")