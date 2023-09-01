import inject
from flask import make_response
from flask_restful import reqparse, Resource
from model.user import User
from config import PersonSession
from utils.timeformat import datetime_to_str
from utils.captcha import generate_verification_code
from utils.auth import manager_login_required


class Test(Resource):
    # method_decorators = [manager_login_required]
    post_parser = reqparse.RequestParser()
    post_parser.add_argument("mobile", type=str, required=True, location="json", help='手机号')
    post_parser.add_argument("name", type=str, required=True, location="json", help='姓名')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument("mobile", type=str, location="args", required=True, help='手机号')

    def get(self):
        args = self.get_parser.parse_args()
        mobile = args.get("mobile")
        # session = inject.instance(PersonSession)
        # user = session.query(User).filter_by(mobile=mobile).first()
        code_img, code_text = generate_verification_code()
        response = make_response(code_img)
        return response

    def post(self):
        args = self.post_parser.parse_args()
        session = inject.instance(PersonSession)
        mobile, name = args.get("mobile"), args.get("name")
        user = User(mobile=mobile, name=name)
        session.add(user)
        session.commit()
        return {"name": user.name, "mobile": user.mobile}
