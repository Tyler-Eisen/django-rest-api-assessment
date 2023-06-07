from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers, status
from tunaapi.views.artist import ArtistSerializer
from tunaapi.views.genre import GenreSerializer
from tunaapi.models import Song, Artist, Genre


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'artist', 'genres', 'title', 'album', 'length')

class SongView(ViewSet):

    def retrieve(self, request, pk):
        """
        Handle GET requests for single Song with associated genres and artist details

        Returns:
        Response -- JSON serialized Song with associated genres and artist details
        """
        song = Song.objects.get(pk=pk)
        serializer = SongSerializer(song)
        data = serializer.data

        # Retrieve artist details
        artist = Artist.objects.get(pk=song.artist_id)
        artist_serializer = ArtistSerializer(artist)
        data['artist'] = artist_serializer.data

        # Retrieve associated genres
        genres = song.genres.all()
        genre_serializer = GenreSerializer(genres, many=True)
        data['genres'] = genre_serializer.data

        return Response(data)

      
    def list(self, request):
      """Handle GET requests to get all Songs
      
      Returns:
          Response -- JSON serialized list of Songs
      """
      artist_id = request.query_params.get('artist_id')
      if artist_id:
          songs = Song.objects.filter(artist_id=artist_id)
      else:
          songs = Song.objects.all()
      
      serializer = SongSerializer(songs, many=True)
      return Response(serializer.data)
    
    def create(self, request):
        artist = Artist.objects.get(pk=request.data["artist"])
        genres = Genre.objects.filter(id__in=request.data.get("genres", []))

        song = Song(
            artist=artist,
            title=request.data["title"],
            album=request.data["album"],
            length=request.data["length"]
        )
        song.save()
        song.genres.set(genres)

        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a song
        
        Returns:
            Response -- Empty body with 204 status code
        """
        song = Song.objects.filter(pk=pk).first()
        song.title = request.data.get("title", song.title)
        song.album = request.data.get("album", song.album)
        song.length = request.data.get("length", song.length)

        # Update the many-to-many relationship with genres
        genre_ids = request.data.get("genres", [])
        genres = Genre.objects.filter(id__in=genre_ids)
        song.genres.set(genres)

        song.save()
        
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
