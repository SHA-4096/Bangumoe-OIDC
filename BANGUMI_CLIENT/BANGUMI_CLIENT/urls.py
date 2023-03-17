"""BANGUMI_CLIENT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bangumi_auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/callback/s',auth_views.auth_callback),
    path('auth/request_code/s',auth_views.request_auth_code),
    path('auth/token_callback/',auth_views.token_callback),
    path('auth/refresh_access_token/',auth_views.refresh_access_token),#POST方法，换取新的access_token
    path('cdn-cgi/styles/main.css',auth_views.dummy),
    path('search/s',auth_views.search),#GET方法，传入keyword即可
    path('get_collection/',auth_views.get_collection),#GET方法,不用参数
    path('mainpage/',auth_views.mainpage),#跳转到主页，不需要参数
    path('bangumoe/view_collection/s',auth_views.bangumoe_view_collection),
    path('bangumoe/delete_collection/s',auth_views.bangumoe_delete_collection),
    path('bangumoe/modify_collection/s',auth_views.bangumoe_modify_collection),
    path('bangumoe/search_collection/s',auth_views.bangumoe_search_collection),
    path('bangumoe/add_collection/s',auth_views.bangumoe_add_collection),
    path('bangumoe/login/s',auth_views.bangumoe_login),
    path('bangumoe/logout/s',auth_views.bangumoe_logout),
    path('bangumoe/usrregister/s',auth_views.bangumoe_register),
]
