
import yampy



class NewsController:

    CLIENT_ID = 'uYWa3hI1V1zvmo8D1R4Iw'
    CLIENT_SECRET = 'hASOpGwVxhj4qQrPjMtTI79q0ZelVcROhpwRvlI'
    REDIRECT_URL = "http://wwww.yandex.ru"

    def __init__(self):
        self.authenticator = yampy.Authenticator(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET)
        pass

    def get_news(self):
        auth_url = self.authenticator.authorization_url(redirect_uri=self.REDIRECT_URL)
        access_token = self.authenticator.fetch_access_token('code')
        print(access_token)
