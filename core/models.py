from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    