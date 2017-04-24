from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SearchCache(models.Model):                   #####
    search_query = models.CharField(max_length=50) #####
    value = models.TextField()                     #####

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=150)
    bio = models.TextField(max_length=500, blank=True)
    email = models.CharField(max_length=50)
    twitter = models.CharField(max_length=50)
