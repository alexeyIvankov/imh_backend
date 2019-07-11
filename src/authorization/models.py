from django.db import models
from django.conf import settings


class UserAccessToken(models.Model):
    token = models.TextField(max_length=1000)
    expiredAt = models.TextField(max_length=500)
    createdAt = models.TextField(max_length=500)

    def __str__(self):
        return self.token


class Auth(models.Model):

    access_token = models.OneToOneField(
        'authorization.UserAccessToken',
        on_delete=models.CASCADE,
        null=True,
        related_name="access_token"
    )

    refresh_token = models.OneToOneField(
        'authorization.UserAccessToken',
        on_delete=models.CASCADE,
        null=True,
        related_name="refresh_token"
    )

    def __str__(self):
        return "auth_token"

class SmsVerification(models.Model):
    code = models.TextField()
    phone = models.TextField()
    date_send = models.TextField()
    device_id = models.TextField()


class RequestAuthorization(models.Model):
    date_create = models.TextField()
    phone = models.TextField()

    sms_verification = models.OneToOneField(
        'authorization.SmsVerification',
        on_delete=models.PROTECT,
        null=True
    )


class TokenModel:
    def __init__(self, token, created_date, expired_date):
        self.token = token
        self.created_date = created_date
        self.expired_date = expired_date
