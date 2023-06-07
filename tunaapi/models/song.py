from django.db import models
from .artist import Artist
from .genre import Genre

class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    album = models.CharField(max_length=50)
    length = models.IntegerField()
