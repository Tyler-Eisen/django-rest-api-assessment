from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers, status
from tunaapi.models import Song, Artist, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'description')

class GenreView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single Genre
        
        Returns:
            Response -- JSON serialized Genre
        """
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)
      
    def list(self, request):
        """Handle GET requests to get all Genres
        
        Returns:
            Response -- JSON serialized list of Genres
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        genre = Genre(
            name=request.data["name"],
            description=request.data["description"]
        )
        genre.save()

        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a genre
        
        Returns:
            Response -- Empty body with 204 status code
        """
        genre = Genre.objects.filter(pk=pk).first()
        genre.name = request.data.get("name", genre.name)
        genre.description = request.data.get("description", genre.description)
        genre.save()

        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """Handle DELETE requests for a genre
        
        Returns:
            Response -- Empty body with 204 status code
        """
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
