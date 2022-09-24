from core.models import WatchlistMovieApiLog


class SaveRequest:
    def __init__(self, get_response):
        self.get_response = get_response
        self.prefixs = [
            '/api/watch-list',
            '/api/watch-list/'
        ]

    def __call__(self, request):
        response = self.get_response(request)

        if not list(filter(request.get_full_path().startswith, self.prefixs)):
            return response

        request_log = WatchlistMovieApiLog(
            username=request.user,
            method=request.method,
            url_path=request.get_full_path(),
            response_code=response.status_code
        )

        # Assign user to log if it's not an anonymous user
        if not request.user.is_anonymous:
            request_log.user = request.user

        # Save log in db
        request_log.save()
        return response
