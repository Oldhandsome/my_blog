from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt import exceptions
# 引入配置文件
from django.conf import settings


class MyAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        salt = settings.SECRET_KEY
        token = request.query_params.get("X-TOKEN")
        try:
            # 集成了用户以及过期时间的验证
            payload = jwt.decode(token, salt, True)
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({"code": 1003, "data": None, "message": "token过期"})
        except jwt.DecodeError:
            raise AuthenticationFailed({"code": 1004, "data": None, "message": "token认证失败"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"code": 1005, "data": None, "message": "token非法"})
        # 认证通过
        # request.user = payload,request.auth = token
        return payload, token


def authenticate_user(function):
    def inner(request, *args, **kwargs):
        salt = settings.SECRET_KEY
        token = request.query_params.get("A-TOKEN")
        try:
            # 集成了用户以及过期时间的验证
            payload = jwt.decode(token, salt, True)
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({"code": 1003, "data": None, "message": "用户token过期"})
        except jwt.DecodeError:
            raise AuthenticationFailed({"code": 1004, "data": None, "message": "用户token认证失败"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"code": 1005, "data": None, "message": "用户token非法"})
        return function(request, *args, **kwargs)

    return inner
