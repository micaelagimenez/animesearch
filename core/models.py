from django.db import models
from django.contrib.auth.models import User


class Anime(models.Model):
    title = models.CharField(max_length=150, unique=True)
    episodes = models.IntegerField()
    image = models.ImageField()
    mal_id = models.IntegerField(null=True)

    def __str__(self):
        return self.title

        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Anime, related_name='favorited_by', null=True, blank=True)
    
    
