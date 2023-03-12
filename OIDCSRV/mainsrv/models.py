from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    nickname=models.CharField(max_length=64)
    profile=models.CharField(max_length=256)
    image=models.CharField(max_length=256)
    usrverified=models.CharField(max_length=16)
    reg_time=models.CharField(max_length=128)
    