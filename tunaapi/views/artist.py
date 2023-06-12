from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import serializers, status
from tunaapi.models import Artist, Song
from tunaapi.serializers import SongSerializer

class ArtistSerializer(serializers.ModelSerializer):
    song_count = serializers.IntegerField(default=None)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count')
        depth = 2

class ArtistView(ViewSet):
  
    def retrieve(self, request, pk):
        """Handle GET requests for single Artist
            
        Returns:
            Response -- JSON serialized Artist
        """
        artist = Artist.objects.annotate(song_count=Count('song')).get(pk=pk)
        serializer = ArtistSerializer(artist)
        
        songs = artist.song_set.all()
        song_serializer = SongSerializer(songs, many=True)
        
        data = serializer.data
        data['songs'] = song_serializer.data

        return Response(data)
      
    def list(self, request):
        """Handle GET requests to get all Artists
        
        Returns:
            Response -- JSON serialized list of Artists
        """
        artists = Artist.objects.annotate(song_count=Count('song'))
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        artist = Artist(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"]
        )
        artist.save()

        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
      """Handle PUT requests for an artist

      Returns:
          Response -- Empty body with 204 status code
        """
      artist = Artist.objects.filter(pk=pk).first()
      artist.name = request.data.get("name", artist.name)
      artist.age = request.data.get("age", artist.age)
      artist.bio = request.data.get("bio", artist.bio)
      artist.save()
      
      serializer = ArtistSerializer(artist)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

      return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        song = Artist.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
