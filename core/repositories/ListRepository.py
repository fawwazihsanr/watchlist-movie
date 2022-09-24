import pdb

from django.db import transaction
from django.forms import model_to_dict
from django_q.tasks import async_task

from core.models import (Watchlist, FavoriteMovieShows, FavoriteTvShows)
from api.clients import get_the_movie_db_client


class ListRepository:
    @staticmethod
    def get_platform_list(media_type, page):
        the_movie_db_client = get_the_movie_db_client()
        response, error = the_movie_db_client.get_list_media(media_type, page)

        if error:
            return error, False

        return response, True

    @staticmethod
    def create_list(data, user):
        with transaction.atomic():
            Watchlist.objects.create(
                username=user,
                description=data['description'],
                name=data['name']
            )

            return 'Success', True

    @staticmethod
    def get_list(user):
        watchlist = Watchlist.objects.filter(username=user, is_deleted=False)
        result = watchlist.values()
        list_result = [entry for entry in result]
        return list_result, True

    @staticmethod
    def get_list_by_id(user, list_id):
        watchlist = Watchlist.objects.filter(watchlist_id=list_id, username=user,
                                             is_deleted=False).last()

        if watchlist:
            movie = FavoriteMovieShows.objects.filter(watchlist=watchlist)
            tv = FavoriteTvShows.objects.filter(watchlist=watchlist)
            movie_result = movie.values()
            tv_result = tv.values()
            movie_list_result = [entry for entry in movie_result]
            tv_list_result = [entry for entry in tv_result]
            dict_watchlist = model_to_dict(watchlist)
            dict_watchlist['movie_list'] = movie_list_result
            dict_watchlist['tv_list'] = tv_list_result
            return dict_watchlist, True

        return 'Id doesnt exist', False

    @staticmethod
    def update_list(data, user, list_id):
        watchlist = Watchlist.objects.filter(watchlist_id=list_id, username=user,
                                             is_deleted=False).last()

        if not watchlist:
            return 'Watchlist doesnt exist', False

        watchlist.description = data['description']
        watchlist.save()

        return 'Updated', True

    @staticmethod
    def delete_list(user, list_id):
        with transaction.atomic():
            watchlist = Watchlist.objects.filter(watchlist_id=list_id, username=user).last()

            if not watchlist:
                return 'Watchlist doesnt exist', False

            watchlist.is_deleted = True
            watchlist.save()
            return 'Deleted', True

    @staticmethod
    def add_item_to_watchlist(user, watchlist_id, datas):
        async_task(ListRepository.save_item, user, watchlist_id, datas)
        # Use the below one if favorite items not added, because sometimes queue not executed.
        # ListRepository.save_item(user, watchlist_id, datas)
        return 'Updated, please see your data', True

    @staticmethod
    def save_item(user, watchlist_id, datas):
        with transaction.atomic():
            the_movie_db_client = get_the_movie_db_client()
            movie = FavoriteMovieShows.objects.filter(watchlist_id=watchlist_id, username=user)
            tv = FavoriteTvShows.objects.filter(watchlist_id=watchlist_id, username=user)

            for data in datas:
                if data['media_type'] == 'movie':
                    response, error = the_movie_db_client\
                        .get_external_movie_id_by_media_id(data['media_id'])
                elif data['media_type'] == 'tv':
                    response, error = the_movie_db_client\
                        .get_external_tv_id_by_media_id(data['media_id'])
                else:
                    return 'Invalid choice', False

                if error:
                    return error, False

                response_details, error_details = the_movie_db_client.get_movie_or_tv_details(
                    response['imdb_id']
                )

                if error_details:
                    return error_details, False

                if data['media_type'] == 'movie':
                    check_movie_is_exist = movie.filter(movie_id=response_details['movie_results'][0]['id']).last()
                    if check_movie_is_exist:
                        continue
                    response_details['movie_results'][0]['movie_id'] = \
                        response_details['movie_results'][0].pop('id')
                    FavoriteMovieShows.objects.create(
                        username=user,
                        watchlist_id=watchlist_id,
                        **response_details['movie_results'][0]
                    )
                elif data['media_type'] == 'tv':
                    check_tv_is_exist = tv.filter(
                        movie_id=response_details['tv_results'][0]['id']).last()
                    if check_tv_is_exist:
                        continue
                    response_details['movie_results'][0]['tv_id'] = \
                        response_details['movie_results'][0].pop('id')
                    FavoriteTvShows.objects.create(
                        username=user,
                        watchlist_id=watchlist_id,
                        **response_details['tv_results'][0]
                    )
