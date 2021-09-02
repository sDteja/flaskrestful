from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='Required field')
_user_parser.add_argument('password', type=str, required=True, help='Required field')


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']) is not None:
            return {'message': 'user exits'}
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'created'}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        user.delete_from_db()
        return {'message': 'user deleted'}, 200


class UserLogin(Resource):

    def post(self):
        request_data = _user_parser.parse_args()
        pwd = request_data.get('password')
        user = UserModel.find_by_username(request_data.get('username'))
        if user and safe_str_cmp(user.password, pwd):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token,
                    "refresh_token": refresh_token}, 200
        return {'message': 'Invalid Credentials'}, 401


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.append(jti)
        return {'message': 'logged out'}, 200
