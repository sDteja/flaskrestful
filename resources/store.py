from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        item = StoreModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'data not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'store exists'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()


class StoreList(Resource):

    def get(self):
        result = StoreModel.find_all()
        if result is not None:
            return {'items': [store.json() for store in result]}
        return {'message': 'no items found'}
