import inject
from flask_restful import reqparse, Resource
from model.user import User
from config import PersonSession
from utils.timeformat import datetime_to_str
from utils.captcha import generate_verification_code
from utils.auth import manager_login_required


class A(Resource):
    # 权限校验
    # method_decorators = [manager_login_required]
    # POST请求要求的参数 type代表类型, required代表是否必填，location参数格式 json/args
    post_parser = reqparse.RequestParser()
    post_parser.add_argument("mobile", type=str, required=True, location="json", help='手机号')
    post_parser.add_argument("name", type=str, required=True, location="json", help='姓名')

    # GET请求要求的参数
    get_parser = reqparse.RequestParser()
    get_parser.add_argument("mobile", type=str, location="args", required=True, help='手机号')

    # GET请求会到这里
    def get(self):
        args = self.get_parser.parse_args()
        mobile = args.get("mobile")
        session = inject.instance(PersonSession)
        user = session.query(User).filter_by(mobile=mobile).first()
        return {"name": user.name,  "mobile": user.mobile}

    # POST请求会到这里
    def post(self):
        # post请求就去取self.post_parser
        args = self.post_parser.parse_args()
        session = inject.instance(PersonSession)
        mobile, name = args.get("mobile"), args.get("name")
        user = User(mobile=mobile, name=name)
        session.add(user)
        session.commit()
        return {"name": user.name, "mobile": user.mobile}
