from rest_framework.views import APIView
from .models import Genre, Anime
from .serializers import GenreSerializer, AnimeSerializer
from rest_framework.response import Response
import requests


class GenreAPIView(APIView):
    def get(self, request):

        url = 'https://api.jikan.moe/v4/genres/anime'
        response = requests.get(url)
        data = response.json()
        genres = data['data']

        for genre_data in genres:
            genre_name = genre_data['name']
            genre_obj, created = Genre.objects.get_or_create(name=genre_name)

        genres_queryset = Genre.objects.all()
        serializer = GenreSerializer(genres_queryset, many=True)
        return Response(serializer.data)


class AnimesAPIView(APIView):
    def get(self, request):
        queryset = Anime.objects.prefetch_related('genre')
        animes = AnimeSerializer(queryset, many=True).data
        # for anime in animes:
        # genres_data = anime['genre']
        # genres = Genre.objects.filter(id__in=genres_data)
        # serializer = GenreSerializer(genres, many=True)
        # anime['genre'] = serializer.data
        return Response(animes)


class AnimeAPIView(APIView):
    def get(self, request, pk):
        try:
            jikan_anime_id = pk
            if not jikan_anime_id:
                return Response({'error': 'Please provide the anime ID'}, status=400)

            anime = Anime.objects.get(jikan_anime_id=jikan_anime_id)
            serializer = AnimeSerializer(anime)
            return Response(serializer.data)
        except Anime.DoesNotExist:
            url = f'https://api.jikan.moe/v4/anime/{pk}'
            response = requests.get(url)
            if response.status_code != 200:
                return Response({'error': 'Failed to fetch anime details from Jikan API'}, status=response.status_code)
            data = response.json()
            anime = data['data']
            genre_ids = []

            for genre in anime.get('genres'):
                print(genre)
                genre_id = Genre.objects.get(name=genre['name'])
                genreSerializer = GenreSerializer(genre_id)
                genre_ids.append(genreSerializer.data['id'])

            mainData = {
                "jikan_anime_id": anime["mal_id"],
                "title": anime.get('title'),
                "description": anime.get('synopsis'),
                "genre": genre_ids,
                "rating": anime.get('score'),
                "episodes": anime.get('episodes'),
            }

            serializer = AnimeSerializer(data=mainData)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
