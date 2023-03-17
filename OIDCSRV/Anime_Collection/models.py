from django.db import models

# Create your models here.

class AnimeCollectionData(models.Model):
    user_id = models.CharField(max_length=256)
    anime_name = models.CharField(max_length=256)
    episode_num = models.CharField(max_length=256)
    director = models.CharField(max_length=256)
    collection_type = models.CharField(max_length=256)
    rating = models.CharField(max_length=256)
    comment = models.TextField()

class AnimeDetailedData(models.Model):
    user_id = models.CharField(max_length=256)
    anime_name = models.CharField(max_length=256)
    episode_num = models.CharField(max_length=256)
    director = models.CharField(max_length=256)
    collection_type = models.CharField(max_length=256)
    rating = models.CharField(max_length=256)
    comment = models.TextField()
    