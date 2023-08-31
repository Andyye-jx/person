from flask import Blueprint
from utils.api import Api
from .test import *

bp = Blueprint("test", __name__, url_prefix="/test")

api = Api(bp)

api.add_resource(Test, "/example")
