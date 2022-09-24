from django.contrib.auth.models import User
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRepository:
    @staticmethod
    def create(data):
        with transaction.atomic():
            try:
                email = User.objects.filter(email=data['email'])
                username = User.objects.filter(username=data['username'])
                if len(email) > 0:
                    return {
                        'message': 'Email already exist',
                        'status': False
                    }

                if len(username) > 0:
                    return {
                        'message': 'User/email is exist!',
                        'status': False
                    }

                data['is_active'] = True
                data['is_superuser'] = False
                user = User(**data)
                user.set_password(data['password'])
                user.save()

                return 'Success', True

            except Exception as exp:
                return {
                    'message': str(exp),
                    'status': False
                }


class CustomJWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }

        user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(
            username=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)
