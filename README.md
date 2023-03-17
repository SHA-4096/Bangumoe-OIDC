# DAY0
调试linux下的开发环境  
学习Django的用法、了解HTTP通信的基本逻辑
# DAY1
使用python的requests库实现了一个测试用client  
实现了邮箱认证链接的生成和用户认证，且如果用户超过规定时间未认证而尝试登录时从数据库中删除对应信息（后期可以加一个定时检查）  
# Day2
实现了对Oauth请求中参数的获取  
实现了简单的用户授权  
实现了授权成功后页面的跳转  
实现了authentication_code,access_token的生成和传递  
(另：花了不少时间解决django orm的makemigrations的冲突问题）  
目前client_id由自己手打的http请求处理  
成功实现了通过token获取server的响应  
# Day3&Day4
解决了access_token_key无法储存的问题  
实现了使用refresh_token更新access_token的功能  
添加了state参数  
添加了对redirection_url的验证  
（另：在这之前我的redirection_url都是直接指向client域名下面的某一个地址，直到现在才知道原来redirection_url不应该分那么细）  
实现了ID_token的颁发  
实现了用户密码的加密存储，增加了说明文档（.well-known/openid-configuration 处访问）  
重定向的状态码改成了301，方便client收到请求之后跳转到自己的路由  
# Day5
实现了番剧管理的功能  
支持模糊搜索  
实现了对登录信息的验证  
# Day6
实现了bangumi的OAuth2.0授权获取  
写了个简单的用户界面  
实现了在bangumi上搜索的功能  
请求中加了state参数  
实现了阶段五进阶内容：好友之间互相看收藏记录（其实改一改就可以变成私信功能？）  
