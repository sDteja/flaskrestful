from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Required field')
    parser.add_argument('store_id', type=float, required=True, help='Required field')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'data not found'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': 'item exists'}, 400
        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'], request_data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred'}, 500
        return item.json(), 201

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, request_data['price'], request_data['store_id'])
        else:
            item.price = request_data['price']
        item.save_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()


class ItemList(Resource):

    def get(self):
        result = ItemModel.query.all()
        if result is not None:
            return {'items': [item.json() for item in result]}
        return {'message': 'no items found'}
