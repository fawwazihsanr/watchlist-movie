from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ModelWithAutoTimestamp(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if self._state.adding:
            self.created = timezone.localtime(timezone.now())
        self.modified = timezone.localtime(timezone.now())
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Watchlist(ModelWithAutoTimestamp):
    username = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='Watchlist', null=True)
    name = models.CharField(max_length=20, null=True)
    watchlist_id = models.AutoField(primary_key=True)
    description = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)


class FavoriteMovieShows(ModelWithAutoTimestamp):
    username = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='FavoriteMovieShow', null=True)
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, db_column='watchlist_id',
                                  null=True)
    poster_path = models.TextField(null=True)
    adult = models.BooleanField(default=False)
    overview = models.TextField(null=True)
    release_date = models.DateField(null=True)
    genre_ids = models.TextField(null=True)
    movie_id = models.IntegerField(null=True)
    original_title = models.TextField(null=True)
    original_language = models.TextField(null=True)
    title = models.TextField(null=True)
    backdrop_path = models.TextField(null=True)
    popularity = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    video = models.BooleanField(default=False)
    vote_average = models.FloatField(null=True)
    media_type = models.TextField(null=True)

    class Meta:
        db_table = 'favorite_movie_shows'


class FavoriteTvShows(ModelWithAutoTimestamp):
    username = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='FavoriteTvShow', null=True)
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, db_column='watchlist_id',
                                  null=True)
    poster_path = models.TextField(null=True)
    popularity = models.FloatField(null=True)
    tv_id = models.IntegerField(null=True)
    backdrop_path = models.TextField(null=True)
    vote_average = models.FloatField(null=True)
    overview = models.TextField(null=True)
    first_air_date = models.DateField(null=True)
    origin_country = models.TextField(null=True)
    genre_ids = models.TextField(null=True)
    original_language = models.TextField(null=True)
    vote_count = models.IntegerField(null=True)
    name = models.TextField(null=True)
    original_name = models.TextField(null=True)
    media_type = models.TextField(null=True)

    class Meta:
        db_table = 'favorite_tv_shows'


class WatchlistMovieApiLog(ModelWithAutoTimestamp):
    username = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='ApiLog', null=True)
    method = models.CharField(max_length=10, null=True)
    url_path = models.CharField(max_length=50, null=True)
    response_code = models.CharField(null=True, max_length=5)

    class Meta:
        db_table = 'watchlist_movie_api_log'
