from django.contrib import admin
from authorization.models import Auth
from authorization.models import UserAccessToken
from django.contrib.auth.models import User, Group



# admin.register(AuthTokens)(admin.ModelAdmin)
# admin.register(UserAccessToken)(admin.ModelAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)