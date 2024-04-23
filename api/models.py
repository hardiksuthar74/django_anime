from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=255)


class Anime(models.Model):
    jikan_anime_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    rating = models.FloatField()
    episodes = models.PositiveIntegerField()
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title
