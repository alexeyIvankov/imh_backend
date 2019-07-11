from rest_framework import serializers
from authorization.models import UserAccessToken
from authorization.models import Auth


class UserAccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccessToken
        fields = ('token', 'expiredAt', 'createdAt')


class AuthTokensSerializer(serializers.ModelSerializer):
    access_token = UserAccessTokenSerializer(many=False)
    refresh_token = UserAccessTokenSerializer(many=False)

    class Meta:
        model = Auth
        fields = ('access_token', 'refresh_token')
