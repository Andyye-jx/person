# -*- coding: utf-8 -*-

class BadParameter(Exception):
    pass


class APIException(Exception):
    error_message = ''
