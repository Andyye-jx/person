# -*- coding: utf-8 -*-
import inject
import jwt as _jwt
import logging
import time
from flask import request, g
from functools import wraps
from utils.exceptions import APIException
from config import Config

logger = logging.getLogger(__name__)
expire_ttl = 24 * 60 * 60 * 7  # 7 day


def jwt_encode(payload, key):
    return _jwt.encode(payload, key=key, algorithm="HS256").decode()


def jwt_decode(jwt, key, **kwargs):
    return _jwt.decode(
        jwt,
        key=key,
        leeway=30,
        options={"verify_exp": True},
        algorithms=["HS256"],
        **kwargs
    )


def jwt_verify(jwt, key, quiet=True):
    payload = {}
    try:
        payload = jwt_decode(jwt, key, verify=True)
        return True, payload
    except _jwt.exceptions.ExpiredSignatureError as e:  # Temporary
        return False, payload
    except Exception as e:
        logger.error("{}: {}".format(e, payload))
        if quiet:
            return False, None
        else:
            raise e


class Token(object):
    name = "token"

    def __init__(self, uid, payload, expire=None, token_type: str = "app"):
        self.uid = uid
        self.payload = payload
        self.expire = expire
        self.token_type = token_type

    @staticmethod
    def generate(uid: int, expire=None):
        iat = int(time.time())
        if expire:
            exp = iat + expire
        else:
            exp = iat + expire_ttl
        payload = {"exp": exp, "iat": iat, "iss": "https://zvip.shop", "uid": uid}
        return Token(uid=uid, payload=payload, expire=expire)

    def encode(self):
        config = inject.instance(Config)
        if self.token_type == "app":
            key = config.app_token_secret_key
        else:
            key = config.admin_token_secret_key
        return jwt_encode(self.payload, key)


@inject.params(config=Config)
def verify_token(config: Config, token_type: str = "app"):
    client_token = request.headers.get(Token.name, "")
    if not client_token:
        raise APIException(10004)  # 没有token
    if token_type == "app":
        key = config.app_token_secret_key
    else:
        key = config.admin_token_secret_key
    valid, payload = jwt_verify(client_token, key)
    if not valid:
        raise APIException(10004)  # 登录状态过期,请重新登录

    uid: int = payload.get("uid")
    g.uid = uid


def user_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_token(token_type="app")
        return func(*args, **kwargs)

    return wrapper


def manager_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_token(token_type="admin")
        return func(*args, **kwargs)

    return wrapper
