from django.urls import path
from .views import GenreAPIView, AnimeAPIView, AnimesAPIView

urlpatterns = [
    path('genres/', GenreAPIView.as_view()),
    path('animes/', AnimesAPIView.as_view()),
    path('anime/<str:pk>', AnimeAPIView.as_view()),
]
