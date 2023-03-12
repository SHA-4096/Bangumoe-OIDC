from django.db import models

# Create your models here.
class OAuthTable(models.Model):
    sitename = models.CharField(max_length=256)
    client_id = models.CharField(max_length=256)
    client_secret = models.CharField(max_length=256)
    redirection_url = models.CharField(max_length=256)
