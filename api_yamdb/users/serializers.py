import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User, USER_ROLES


def validate_username(username: str) -> None:
    if username.lower() == 'me':
        raise serializers.ValidationError(
            'Имя пользователя не может быть ME.'
        )
    if re.search(r'[^\w+._@-]', username):
        raise serializers.ValidationError(
            'В имени пользователя разрешены буквы, цифры и @/./+/-/_'
        )


class SingUpSerializer(serializers.Serializer):
    username = CharField(max_length=150, required=True)
    email = EmailField(max_length=254, required=True)

    def validate(self, attrs):
        validate_username(attrs['username'])
        user = User.objects.filter(username=attrs['username']).first()

        if not user:
            try:
                user = User.objects.create_user(**attrs)
            except IntegrityError as error:
                raise serializers.ValidationError(
                    str(error)
                )
        elif user.email != attrs['email']:
            raise serializers.ValidationError(
                'У пользователя другой Email.'
            )

        confirmation_code = str(RefreshToken.for_user(user))
        send_mail(
            subject='YaMDb код подтверждения',
            message=f'Код подтверждения: {confirmation_code}',
            recipient_list=[attrs['email']],
            from_email=settings.EMAIL_HOST_USER,
        )
        return attrs


class TokenGetSerializer(serializers.Serializer):
    username = CharField(max_length=150, required=True)
    confirmation_code = CharField(required=True)

    def validate(self, attrs):
        get_object_or_404(get_user_model(), username=attrs['username'])
        data: dict = {'username': attrs['username']}

        try:
            refresh = RefreshToken(attrs['confirmation_code'])
        except TokenError:
            raise serializers.ValidationError(
                'Неверный код подтверждения.'
            )
        data['token'] = str(refresh.access_token)
        return data


class UserSerializer(serializers.ModelSerializer):
    username = CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = CharField(max_length=150, required=False)
    last_name = CharField(max_length=150, required=False)
    role = serializers.ChoiceField(USER_ROLES, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate(self, attrs):
        if attrs.get('username'):
            validate_username(attrs['username'])
        return attrs
