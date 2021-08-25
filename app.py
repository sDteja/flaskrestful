from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.item import Item, ItemList
from security import Authenticate
from resources.user import UserRegister
from resources.store import Store, StoreList
from db import db

app = Flask('__name__')
app.config["JWT_SECRET_KEY"] = "test"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

api.add_resource(Authenticate, "/auth")
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
