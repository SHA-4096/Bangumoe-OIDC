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
    path('token_get_success/s',clientview.token_get_success),
    path('ID_token_request/s',clientview.ID_token_request),
    path('ID_token_responded/s',clientview.ID_token_responded),#成功拿到IDtoken
    
]
