from django.contrib import admin
from news.models import NewsGroup
from news.models import News
from news.models import NewsAttach

# Register your models here.
class NewsGroupAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Описание', {
            'fields': ('name', 'date_created')
        }),
        ('Подробнее..', {
            'classes': ('collapse',),
            'fields': ('description',)
        }),
    )

    list_display = ['name', 'date_created']
    search_fields = ('name', 'description', 'date_created',)


class NewsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Описание', {
            'fields': ('news_id','group', 'body')
        }),
        ('Подробнее..', {
            'classes': ('collapse',),
            'fields': ('sender_id','date_created', 'last_update')
        }),
    )

    list_display = ['group','body', 'date_created']
    search_fields = ('body', 'news_id', 'date_created',)



class NewsAttachesAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Описание', {
            'fields': ('attach_id','name', 'type', 'url', 'news', 'size')
        }),
        ('Подробнее..', {
            'classes': ('collapse',),
            'fields': ('preview_url',)
        }),
    )

    list_display = ['name', 'attach_id', 'type', 'url']
    search_fields = ('name', 'attach_id', 'type', 'url',)


admin.site.register(News, NewsAdmin)
admin.site.register(NewsAttach, NewsAttachesAdmin)
admin.site.register(NewsGroup, NewsGroupAdmin)
