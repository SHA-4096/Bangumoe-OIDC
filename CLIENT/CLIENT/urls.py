"""CLIENT URL Configuration

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
from clientsrv import views as clientview
urlpatterns = [
    path('admin/', admin.site.urls),
    path('redir_auth/s',clientview.auth_success),
    path('auth_request/s',clientview.send_auth_request),#传入sitename,client_id,state,client_secret,redirection_url
    path('token_get_success/s',clientview.token_get_success),#拿到access_token,refresh_token,ID_token\ID_token_key和iss
    path('ID_token_request/s',clientview.ID_token_request),#命名问题，实际上这两个是用access_token请求资源，和ID_token无关
    path('ID_token_responded/s',clientview.ID_token_responded),#成功得到响应
    path('refresh_access_token/s',clientview.refresh_access_token),#传入client_id,refresh_token
    path('access_token_refreshed/s',clientview.access_token_refreshed),#获取到新的access_token之后的处理
    
]
