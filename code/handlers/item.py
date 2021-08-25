import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be nil")

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'an error occurred'}, 500
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'{name} already exists'}, 400
        
        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occurred"}, 500

        return item.json(), 201


    def delete(self, name):
        if ItemModel.find_by_name(name) is None:
            return {'message': f'{name} does not exist'}, 400
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': f'{name} has been deleted'}


    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except Exception:
                return {'message': 'an error occurred'}, 500
        else:
            try:
                updated_item.update()
            except Exception:
                return {'message': 'an error occurred'}, 500
        return updated_item.json()
        


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        
        items = []
        for row in result:
            items.append({'name': row[0],'price': row[1]})
        
        connection.close()
        return {'items': items}