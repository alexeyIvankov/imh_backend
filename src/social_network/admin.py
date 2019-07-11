from django.contrib import admin
from django.contrib import messages
from .models import SocialNetworkSite
from django.http.response import HttpResponseRedirect
from social_network.api.controllers.social_network_controller import SocialNetworkController
import core.api.binding_conf.binding_conf
import inject

class SocialNetworkAdmin(admin.ModelAdmin):
    add_form_template = 'admin/change_form.html'
    change_form_template = "admin/change_form_social_network.html"
    social_network_controller = inject.instance(SocialNetworkController)

    list_display = ['name']
    search_fields = ('name',)

    def response_change(self, request, obj):
        if "activation-button" in request.POST:
            return self.handle_activation_button_pressed(request,obj)
        return super().response_change(request, obj)


    fieldsets = (
        ('Описание', {
            'fields': ('name',)
        }),
        ('Подробнее..', {
            'classes': ('collapse',),
            'fields': ('token',)
        }),
    )

    def handle_activation_button_pressed(self, request, obj):

        if obj.name == 'yammer':
            auth_url = self.social_network_controller.yammer_service.generate_auth_url()
            return HttpResponseRedirect(auth_url)
        else:
            messages.error(request, 'Выбранная соц сеть еще не настроена')
            return HttpResponseRedirect(request.get_full_path())


    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(SocialNetworkSite, SocialNetworkAdmin)