from django.conf import settings
import requests


def get_the_movie_db_client():
    return TheMovieDbClient(
        settings.THE_MOVIE_DB_BASE_URL_V3,
        settings.THE_MOVIE_DB_API_KEY_V3
    )


class TheMovieDbClient(object):
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def send_request(self, request_type, request_path, data=None, params=None):
        request_params = {
            'url': "%s%s" % (self.base_url, request_path),
            'json': data,
            'params': {'api_key': self.api_key}
        }

        if params:
            request_params['params'].update(params)

        return_response = None
        try:
            requests_ = eval('requests.%s' % request_type)
            response = requests_(**request_params)
            return_response = response.json()
            response.raise_for_status()
            error = None
            error_message = None
        except Exception as e:
            error = str(e)
            error_message = error

        return return_response, error_message

    def get_list_movie(self, page):
        return self.send_request('get', '/discover/movie', params={'page': page})

    def get_external_movie_id_by_media_id(self, media_id):
        return self.send_request('get', '/movie/{}/external_ids'.format(media_id))

    def get_external_tv_id_by_media_id(self, media_id):
        return self.send_request('get', '/tv/{}/external_ids'.format(media_id))

    def get_movie_or_tv_details(self, external_id):
        return self.send_request('get', '/find/{}'.format(external_id), params={
            'external_source': 'imdb_id'})
