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
