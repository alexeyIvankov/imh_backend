from django.db import models
from social_network.types import *
from news.models import News


class SocialNetworkSite(models.Model):
    class Meta:
        verbose_name_plural = 'Все социальные сети'

    name = models.CharField(max_length=30,
                            choices=SOCIAL_NETWORK_TYPE,
                            default='yammer',
                            primary_key=True)

    token = models.TextField(blank=True)


class SocialNetwork(models.Model):

    social_network_site = models.ForeignKey(
        'social_network.SocialNetworkSite',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        blank=False,
    )

    news = models.ForeignKey(
        'news.News',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        blank=False,
        related_name="news"
    )