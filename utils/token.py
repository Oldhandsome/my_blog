import jwt
import datetime
from django.conf import settings


def create_token(payload, exp):
    # 自定义的盐 ，即随机字符串
    salt = settings.SECRET_KEY
    headers = {
        "typ": 'jwt',
        "alt": 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=exp)
    token = jwt.encode(payload=payload, key=salt, headers=headers).decode('utf-8')
    return token
