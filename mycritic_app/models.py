from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SearchCache(models.Model):                   #####
    search_query = models.CharField(max_length=50) #####
    value = models.TextField()                     #####

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, primary_key=True)
    movies_rated = models.PositiveIntegerField(default=0)
    bio = models.TextField(max_length=500, blank=True)
    email = models.CharField(max_length=50)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)

    def add_rating():
        movies_rated += 1

    def remove_rating():
        return

    def get_rated():
        return movies_rated

class Movie(models.Model):
    identifier = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    poster = models.CharField(max_length=50)
    description = models.TextField()

    def create(cls, identifier, title, poster, description):
        movie = cls(identifier=identifier,
                    title=title,
                    poster=poster,
                    description=description)
        return movie

class Rating(models.Model):
    identifier = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    movie_id = models.CharField(max_length=50)
    rating = models.CharField(max_length=30)
