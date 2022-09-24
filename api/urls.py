from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views
from core.repositories.UserRepository import CustomJWTSerializer

urlpatterns = [
    path('login', TokenObtainPairView.as_view(serializer_class=CustomJWTSerializer),
         name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', csrf_exempt(views.register), name='register'),
    path('watch-list', csrf_exempt(views.WatchList.as_view()), {'list_id': None}, name='watch-list'),
    path('watch-list/<int:list_id>', csrf_exempt(views.WatchList.as_view()), name='watch-list'),
    # Items
    path('watch-list/<int:list_id>/items', csrf_exempt(views.WatchlistItem.as_view()), name='watch-list-items',),
]
