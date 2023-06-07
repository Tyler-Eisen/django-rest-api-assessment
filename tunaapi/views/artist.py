from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count')

class ArtistView(ViewSet):
  
    def retrieve(self, request, pk):
        """Handle GET requests for single Artist
            
        Returns:
            Response -- JSON serialized Artist
        """
        artist = Artist.objects.get(pk=pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)
      
    def list(self, request):
        """Handle GET requests to get all Artists
        
        Returns:
            Response -- JSON serialized list of Artists
        """
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        artist = Artist(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
            song_count=request.data["song_count"]
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
      artist.song_count = request.data.get("song_count", artist.song_count)
      artist.save()
      
      serializer = ArtistSerializer(artist)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

      return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        song = Artist.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
