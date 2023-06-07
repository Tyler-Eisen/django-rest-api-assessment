from django.db import models

class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    bio = models.TextField()
    song_count = models.IntegerField()
    
