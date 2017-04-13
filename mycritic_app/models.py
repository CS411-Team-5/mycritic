from django.db import models

# Create your models here.
class SearchCache(models.Model):                   #####
    search_query = models.CharField(max_length=50) #####
    value = models.TextField()                     #####
