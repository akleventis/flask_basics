from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import RegisterUser
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'secret_key'
api = Api(app) # https://flask-restful.readthedocs.io/en/latest/api.html#id1

jwt = JWT(app, authenticate, identity) # /auth

# ENDPOINTS
api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
api.add_resource(RegisterUser, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)