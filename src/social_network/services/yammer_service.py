import yampy
from imh_corp_server.settings import *
from django.conf import settings
from social_network.types import *
from .db_service import DBServiceSocialNetwork


class YammerService:

    REDIRECT_URI = HOST_URL + SOCIAL_NETWORK['yammer']['redirect_url']
    CLIENT_SECRET = SOCIAL_NETWORK['yammer']['client_secret']
    CLIENT_ID = SOCIAL_NETWORK['yammer']['client_id']

    def __init__(self):
        self.authenticator = yampy.Authenticator(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET)
        self.db_service = DBServiceSocialNetwork()

    def is_auth(self):
        yammer_site_model = self.db_service.try_get_social_network_site(name='yammer')
        if yammer_site_model == None or yammer_site_model.token == None:
            return False
        return  True

    def get_access_token(self):
        yammer_site_model = self.db_service.try_get_social_network_site(name='yammer')
        return yammer_site_model.token


    def generate_auth_url(self):
        return self.authenticator.authorization_url(redirect_uri=self.REDIRECT_URI)

    def try_set_or_update_authorization(self, code):

        access_data = self.authenticator.fetch_access_data(code=code)
        if access_data == None:
            raise Exception('access_data is empty')

        token = access_data['access_token']['token']
        if token == None:
            raise Exception('token is empty')

        self.db_service.try_create_or_update_social_network_access_token(name='yammer', access_token=token)

    def try_get_groups(self):
        if self.is_auth() == False:
            return None

        yammer = yampy.Yammer(access_token=self.get_access_token())
        groups = yammer.client.get("/groups")

        return groups

    def try_get_messages(self, group_id,
                         newest_message_id=None,
                         oldest_message_id=None):

        if self.is_auth() == False:
            return None

        yammer = yampy.Yammer(access_token=self.get_access_token())

        if newest_message_id != None:
            params = {'newer_than': newest_message_id}
        elif oldest_message_id != None:
            params = {'older_than': oldest_message_id}
        else:
            params = {}

        messages = yammer.client.get('/messages/in_group/'+ group_id,  **params)

        return  messages

