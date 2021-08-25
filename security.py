from models.user import UserModel
from flask import request
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token


class Authenticate(Resource):

    def post(self):
        request_data = request.get_json()
        pwd = request_data.get('password')
        user = UserModel.find_by_username(request_data.get('username'))
        if user and safe_str_cmp(user.password, pwd):
            return {"token": create_access_token(identity=user.username)}

