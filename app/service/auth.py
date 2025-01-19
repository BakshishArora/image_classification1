import jwt
import datetime
from datetime import timezone
from app.config import Config

class Authorize:
    
    @classmethod
    def encrypt(cls, username):
        paylaod = {
            "username": username,
            "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=300)
        }
        token = jwt.encode(paylaod, Config.SECRET_KEY, algorithm='HS256')
        return token
    
    @classmethod
    def decrypt(cls, token):
        try:
            paylaod = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256')
            return paylaod
        except jwt.ExpiredSignatureError:
            return "error"
        except jwt.InvalidTokenError:
            return "error"
        