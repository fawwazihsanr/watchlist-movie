from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=10)


class SessionSerializer(serializers.Serializer):
    request_token = serializers.CharField()


class CreateListSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    description = serializers.CharField(allow_blank=True, default='')


class UpdateListSerializer(serializers.Serializer):
    description = serializers.CharField()


class AddItemsSerializer(serializers.Serializer):
    media_type = serializers.CharField()
    media_id = serializers.IntegerField()
