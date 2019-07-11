from django.db import models
from core.api.json.json_presentation import JSONPresentation

# Create your models here.
class NewsGroup(models.Model, JSONPresentation):
    class Meta:
        verbose_name_plural = 'Все группы'

    group_id = models.IntegerField(primary_key=True)
    type = models.TextField(max_length=200,
                            null=False)

    name = models.TextField(verbose_name='Название',
                            null=False)

    description = models.TextField(verbose_name='Описание',
                                   null=True)

    date_created = models.BigIntegerField(null=True)
    last_update_messages = models.BigIntegerField(null=True)

    def json(self):
        json = {}

        json['id'] = self.group_id
        json['name'] = self.name
        json['type'] = self.type

        if self.description != None:
            json['description'] = self.description

        if self.date_created != None:
            json['date_created'] = self.date_created

        return json

class NewsAttach(models.Model, JSONPresentation):
    class Meta:
        verbose_name_plural = 'Все файлы'

    attach_id = models.IntegerField(primary_key=True)
    name = models.TextField(null=False)
    type = models.TextField(null=False)
    url = models.TextField(null=False)
    content_type = models.TextField(null=False)
    date_created = models.BigIntegerField()

    preview_url = models.TextField(null=True)
    large_icon_url = models.TextField(null=True)
    small_icon_url = models.TextField(null=True)
    content_class = models.TextField(null=True)
    size = models.IntegerField(null=True)

    news = models.ForeignKey('News',
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='attach_news')

    def json(self):
        json = {}

        json['id'] = self.attach_id
        json['name'] = self.name
        json['type'] = self.type
        json['url'] = self.url
        json['content_type'] = self.content_type
        json['date_created'] = self.date_created

        if self.preview_url != None:
            json['preview_url'] = self.preview_url

        if self.large_icon_url != None:
            json['large_icon_url'] = self.large_icon_url

        if self.small_icon_url != None:
            json['small_icon_url'] = self.small_icon_url

        if self.content_class != None:
            json['content_class'] = self.content_class

        if self.size != None:
            json['size'] = self.size

        return json

class News(models.Model, JSONPresentation):
    class Meta:
        verbose_name_plural = 'Все новости'

    news_id = models.IntegerField(primary_key=True)

    group = models.ForeignKey('NewsGroup',
                             on_delete=models.CASCADE,
                             null=True,
                             related_name='news_group')


    sender_id = models.IntegerField()
    date_created = models.BigIntegerField()
    body = models.TextField(null=False)
    last_update = models.BigIntegerField(null=True)

    def json(self):
        json = {}

        json['id'] = self.news_id
        json['sender_id'] = self.sender_id
        json['date_created'] = self.date_created
        json['body'] = self.body

        if self.last_update != None:
            json['last_update'] = self.last_update

        json['group'] = self.group.json()

        return json