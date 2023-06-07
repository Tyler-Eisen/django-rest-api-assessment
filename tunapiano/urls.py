from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from tunaapi.views import SongView, ArtistView, GenreView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'songs', SongView, 'gametype')
router.register(r'artists', ArtistView, 'artist')
router.register(r'genres', GenreView, 'genre')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
