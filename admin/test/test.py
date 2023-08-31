import inject
from flask_restful import reqparse, Resource
from model.user import User
from config import PersonSession
from utils.timeformat import datetime_to_str


class Test(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument("mobile", type=str, required=True, location="json", help='手机号')
    post_parser.add_argument("name", type=str, required=True, location="json", help='姓名')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument("mobile", type=str, location="args", required=True, help='手机号')

    def get(self):
        args = self.get_parser.parse_args()
        mobile = args.get("mobile")
        session = inject.instance(PersonSession)
        user = session.query(User).filter_by(mobile=mobile).first()
        return {"name": user.name, "mobile": user.mobile, "created_at": datetime_to_str(user.created_at)}

    def post(self):
        args = self.post_parser.parse_args()
        session = inject.instance(PersonSession)
        mobile, name = args.get("mobile"), args.get("name")
        user = User(mobile=mobile, name=name)
        session.add(user)
        session.commit()
        return {"name": user.name, "mobile": user.mobile}
