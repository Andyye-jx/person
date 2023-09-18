from flask import Blueprint
from utils.api import Api
from .person import *

bp = Blueprint("person", __name__, url_prefix="/person")

api = Api(bp)
# /person/info GET 请求 代表获取列表
# /person/info POST 请求 代表新增
# 由于前缀写了/person，所以请求里面直接写后续路径就行
api.add_resource(A, "/info")
