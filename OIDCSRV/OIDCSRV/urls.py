"""OIDCSRV URL Configuration

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
from mainsrv import views
from OAuthapp import views as views_Oauth
urlpatterns = [
    path('admin/', admin.site.urls),
    path('usrlogin/',views.usrlogin,name = 'login'),
    path('usrregister/',views.usrregister,name = 'registration'),
    path('register-verify/s',views.verify,name = 'verification'),
    path('get_clientrequest/s',views_Oauth.get_clientrequest,name = 'get_clientrequest'),
    path('auth/s',views_Oauth.user_authenticate,name = 'userauthenticate'),
    path('auth2/s',views_Oauth.user_authenticate2,name = 'userauthenticate2'),#接收HS256加密的code和client_secret
    path('access_token_request/s',views_Oauth.access_token_request,name = 'access_token_request'),#请求access_token:传入HS256加密的code，内含auth_code，redirection_url以及client_id，当然还会传入client_secret
    path('query_with_access_token/s',views_Oauth.query_with_access_token)#用户传入HS256加密的code[client_id,access_token]，还有client_secret，返回一个加密后的串以及secret_key
#    path('login/',views.listen),
#    path('submit/', views.submit_form, name='submit_form'),
]
