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
from Anime_Collection import views as views_Anime
urlpatterns = [
    #用户账户相关
    path('admin/', admin.site.urls),
    path('usrlogin/',views.usrlogin,name = 'login'),#POST方法，传入name、password、client_id(其实传输也应该要加密但是现在还没做)
    path('usrlogout/s',views.usrlogout,name = 'logout'),#POST方法，传入name(即user_id)、client_id
    path('usrregister/',views.usrregister,name = 'registration'),#POST方法，传入name,password,email,nickname,profile,image
    path('usrmodify/',views.usrmodify),#POST方法，传入name,password,email,nickname,profile,image
    path('register-verify/s',views.verify,name = 'verification'),#邮件验证
    path('check_online_state/s',views.check_online_state),#GET方法，验证这个client是否登入了相应的用户，传入client_id和name，返回一个Httpresponse，其为True或False(字符串)
    #OIDC相关
    path('get_clientrequest/s',views_Oauth.get_clientrequest,name = 'get_clientrequest'),
#    path('auth/s',views_Oauth.user_authenticate,name = 'userauthenticate'),
    path('auth2/s',views_Oauth.user_authenticate2,name = 'userauthenticate2'),#auth_endpoint
    path('access_token_request/s',views_Oauth.access_token_request,name = 'access_token_request'),#请求access_token:传入HS256加密的code，内含auth_code，redirection_url以及client_id，当然还会传入client_secret
    path('query_with_access_token/s',views_Oauth.query_with_access_token),#用户传入HS256加密的code[client_id,access_token]，还有client_secret，返回一个加密后的串以及secret_key
    path('renew_access_token/s',views_Oauth.renew_access_token),#传入HS256加密的code[client_id],以及client_secret,refresh_token,redirection_url,返回一个access_token
    path('.well-known/openid-configuration',views_Oauth.doc_show),#文档说明
    #番剧收藏相关
    path('anime/collect_anime/s',views_Anime.collect_anime),#(POST方法)收藏番剧，传入user_id,client_id,anime_name,episode_num,director,collection_type,rating,comment
    path('anime/collect_anime_detail_sync/s',views_Anime.collect_anime_deail_sync),#POST方法，和上面一样的参数，用来获取Bangrumi上面的单个观看状态
    path('anime/modify_collection/s',views_Anime.modify_collection),#POST方法，传跟collect_anime同样的参数
    path('anime/delete_collection/s',views_Anime.delete_collection),#GET方法，传入user_id,client_id,anime_name
    path('anime/search_collection/s',views_Anime.search_collection),#GET方法，传入user_id,client_id,anime_name
    path('anime/view_collections/s',views_Anime.view_collections),#GET方法，传入user_id,client_id,返回用户的所有收藏的列表
    path('anime/collection_data/s',views_Anime.collection_data),#GET方法，传入user_id,client_id和anime_name，显示番剧详细信息
    path('anime/add_friend/',views_Anime.add_friend),#POST,添加好友，传入user_id,client_id,friend_id
    path('anime/send_dataflow/',views_Anime.send_dataflow),#POST,发消息给用户，传入content,user_id,client_id
    path('anime/check_dataflow/',views_Anime.check_dataflow),#POST,检查信息,传入user_id,client_id,返回一个text
]   