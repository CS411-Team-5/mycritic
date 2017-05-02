from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

# Create your models here.
class SearchCache(models.Model):                   #####
    search_query = models.CharField(max_length=50) #####
    value = models.TextField()                     #####

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=150)
    movies_rated = models.PositiveIntegerField(default=0)
    #profile_photo = models.CharField()
    email = models.CharField(max_length=50)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)
    similarity_scores = models.TextField(blank=True)

    def add_rating():
        movies_rated += 1

    def remove_rating():
        return

    def get_rated():
        return movies_rated

    def __str__(self):
        return str(self.user)

class MovieManager(models.Manager):

    def create_movie(self, iden, title, poster, description, genres):
        new_movie = self.update_or_create(identifier=iden,
                                          title=title,
                                          poster=poster,
                                          description=description,
                                          genre_list=str(genres))
        return new_movie

class Movie(models.Model):
    identifier = models.PositiveIntegerField(default=0, primary_key=True)
    title = models.CharField(max_length=100)
    poster = models.CharField(max_length=50)
    description = models.TextField()
    genre_list = models.TextField(default='[]')

    objects = MovieManager()

    def __str__(self):
        return self.title

class RatingManager(models.Manager):
    
    def create_rating(self, user, movie, raw_rating, user_auth):
        rating_map = {'5': 5.0,
                      '4 and a half': 4.5,
                      '4': 4.0,
                      '3 and a half': 3.5,
                      '3': 3.0,
                      '2 and a half': 2.5,
                      '2': 2.0,
                      '1 and a half': 1.5,
                      '1': 1.0,
                      'half': 0.5}
        num_rating = rating_map[raw_rating]
        new_rating = None
        rate_filter = self.filter(user_id=user, movie_id=int(movie))
        if len(rate_filter) != 0:
            new_rating = rate_filter[0]
            new_rating.rating = num_rating
            new_rating.save()
        else:
            new_rating = self.create(user_id=user, movie_id=int(movie), rating=num_rating)
            profile = UserProfile.objects.filter(user=user_auth).update(movies_rated = F('movies_rated') + 1)

        return new_rating

class Rating(models.Model):
        
    identifier = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    movie_id = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0)

    objects = RatingManager()

    def __str__(self):
        return self.user_id + " rating of " + str(self.movie_id)
