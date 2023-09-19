from flask import Blueprint
from utils.api import Api
from .other import *

# url_prefix 通用路径，可以不写
bp = Blueprint("other", __name__, url_prefix="")

api = Api(bp)
# url_prefix为空的话，这里要访问/other/setting，就得
# api.add_resource(B, "/other/setting")
