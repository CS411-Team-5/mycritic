from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SearchCache(models.Model):                   #####
    search_query = models.CharField(max_length=50) #####
    value = models.TextField()                     #####

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    movies_rated = models.PositiveIntegerField(default=0)
    bio = models.TextField(max_length=500, blank=True)
    email = models.CharField(max_length=50)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)

    def add_rating():
        return

    def remove_rating():
        return

    def get_rated():
        return movies_rated
