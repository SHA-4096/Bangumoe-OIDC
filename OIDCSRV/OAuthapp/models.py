from django.db import models

# Create your models here.
class OAuthTable(models.Model):
    sitename = models.CharField(max_length=256)
    client_id = models.CharField(max_length=256)
    client_secret = models.CharField(max_length=256)
    authed_uid = models.CharField(max_length=256)#授权用户的uid
    auth_code = models.CharField(max_length=256)
    auth_code_expired = models.CharField(max_length=256)
    access_token_key = models.CharField(max_length=256)
    refresh_token_key = models.CharField(max_length=256)
    redirection_url = models.CharField(max_length=256)