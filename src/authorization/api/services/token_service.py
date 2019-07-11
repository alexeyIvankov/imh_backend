import jwt
from datetime import datetime, timedelta, time
from authorization.models import TokenModel


class TokenService:

    def __init__(self):
        self.secret = '9CED90D4BF797FEF67BF0AD46A8C5A1A4B7E65E47F09675F8547A5C553AEF597'
        self.jwt_algoritm = 'HS256'
        self.life_time_access_token = 24 #hours
        self.life_time_refresh_token = 30  #days

    def generate_access_token(self, login, device_id):

        exp_date: datetime = (datetime.utcnow() + timedelta(hours=self.life_time_access_token)).timestamp().__round__()
        created_date = datetime.utcnow().timestamp().__round__()

        payload = {
            'type': 'access',
            'login': login,
            'device_id': device_id,
            'exp': exp_date,
            'created': created_date
        }

        token = jwt.encode(payload=payload, key=self.secret, algorithm=self.jwt_algoritm)
        token_str = token.decode("utf-8")
        token_model = TokenModel(token_str, created_date, exp_date)
        return token_model

    def generate_refresh_token(self, device_id):

        exp_date = (datetime.utcnow() + timedelta(days=self.life_time_refresh_token)).timestamp().__round__()
        created_date = datetime.utcnow().timestamp().__round__()

        payload = {
            'type': 'refresh',
            'exp': exp_date,
            'device_id': device_id,
            'created': created_date
        }

        token = jwt.encode(payload=payload, key=self.secret, algorithm=self.jwt_algoritm)
        token_str =  token.decode("utf-8")
        token_model = TokenModel(token_str, created_date, exp_date)
        return token_model






