from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'secret_key'
api = Api(app) # https://flask-restful.readthedocs.io/en/latest/api.html#id1

jwt = JWT(app, authenticate, identity) # /auth

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be nil")

    # @jwt_required()
    def get(self, name):
        item = [x for x in items if name==x['name']]
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if [x for x in items if name==x['name']]:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        item = [x for x in items if name==x['name']]
        if item:
            items.remove(item[0])
            return {'message': 'item \'{}\' has been deleted'.format(item[0]['name'])}
        return "{} not found".format(name), 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = [x for x in items if name==x['name']]
        if not item:
            item = {'name': name, 'price': data['price']}
            items.append(item)
            return item, 201
        else:
            item[0].update(data)
        return item[0]


class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)