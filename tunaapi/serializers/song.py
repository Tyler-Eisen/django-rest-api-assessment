from rest_framework import serializers
from tunaapi.models import Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'artist', 'genres', 'title', 'album', 'length')
