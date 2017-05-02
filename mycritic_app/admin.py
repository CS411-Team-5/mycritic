from django.contrib import admin

# Register your models here.

from .models import Movie, Rating, UserProfile

admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(UserProfile)
