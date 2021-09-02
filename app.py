import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from blacklist import BLACKLIST
from resources.item import Item, ItemList
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.store import Store, StoreList
from db import db

app = Flask('__name__')
app.config["JWT_SECRET_KEY"] = "test"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL_NEW', "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'test'

api = Api(app)


# @app.before_first_request
# def create_tables():
#     db.create_all()

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST
#
#
# @jwt.additional_claims_loader
# def add_claims_jwt(identity):
#     if identity == 1:
#         return {'is_admin': True}
#     return {'is_admin': False}
#
#
# @jwt.expired_token_loader
# def expired_token_callback(jwt_header, jwt_payload):
#     return jsonify({
#         'description': 'token has expired',
#         'error': 'token_expired'
#     }), 401
#
#
# @jwt.invalid_token_loader
# def invalid_token_callback(jwt_header, jwt_payload):
#     return jsonify({
#         'description': 'signature verification failed'
#     }), 401


api.add_resource(UserLogin, "/auth")
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
