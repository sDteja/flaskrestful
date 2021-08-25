import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Required field')
    parser.add_argument('password', type=str, required=True, help='Required field')

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']) is not None:
            return {'message': 'user exits'}
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'created'}, 201

