from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from api.serializers import (
    RegisterSerializer,
    CreateListSerializer,
    UpdateListSerializer,
    AddItemsSerializer
)
from core.repositories import (UserRepository, ListRepository)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    message, valid = UserRepository.create(data)

    if not valid:
        return Response(
            data={'message': message},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        data={'message': message},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_media_list(request):
    page = request.GET.get('page', 1)
    media_type = request.GET.get('media_type', 'movie')
    message, valid = ListRepository.get_platform_list(media_type, page)

    if not valid:
        return Response(
            data={'message': message},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        data={'message': message},
        status=status.HTTP_201_CREATED
    )


class WatchList(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, list_id=None):
        serializer = CreateListSerializer
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        message, valid = ListRepository.create_list(data, request.user)

        if not valid:
            return Response(
                data={'message': message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data={'message': message},
            status=status.HTTP_201_CREATED
        )

    def get(self, request, list_id=None):
        if list_id:
            message, valid = ListRepository.get_list_by_id(request.user, list_id)
        else:
            message, valid = ListRepository.get_list(request.user)

        if not valid:
            return Response(
                data={'message': message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=message,
            status=status.HTTP_200_OK
        )

    def put(self, request, list_id):
        serializer = UpdateListSerializer
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        message, valid = ListRepository.update_list(data, request.user, list_id)

        if not valid:
            return Response(
                data={'message': message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data={'message': message},
            status=status.HTTP_200_OK
        )

    def delete(self, request, list_id):
        message, valid = ListRepository.delete_list(request.user, list_id)

        if not valid:
            return Response(
                data={'message': message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data={'message': message},
            status=status.HTTP_200_OK
        )


class WatchlistItem(APIView):
    permission_classes = (IsAuthenticated,)
    serializer = AddItemsSerializer

    def post(self, request, list_id):
        serializer = self.serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        message, valid = ListRepository.add_item_to_watchlist(request.user, list_id, data)

        if not valid:
            return Response(
                data={'message': message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data={'message': message},
            status=status.HTTP_201_CREATED
        )
