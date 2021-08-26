from datetime import timedelta
from flask import Flask
from flask.json import jsonify
from flask_restful import Api
from flask_jwt import JWT
from db import db

from security import authenticate, identity
from resources.user import RegisterUser
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# Where to find data.db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # root foler in project
app.secret_key = 'secret_key'
api = Api(app) # https://flask-restful.readthedocs.io/en/latest/api.html#id1

# Create tables before first request
@app.before_first_request
def create_tables():
    db.create_all()

# config sql_alchemy, turns off flask_sqlalchemy mod tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# endpoint /auth to /login
app.config['JWT_AUTH_URL_RULE'] = '/login'
# JWT expire time to ten minutess
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds = 3600)
# Auth key name to email instead of 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

# To return id in response body along with token
jwt = JWT(app, authenticate, identity)
@jwt.auth_response_handler
def response_handler(access_token, identity):
    return jsonify({'token': access_token.decode('utf-8'), 'user': identity.id})

# ENDPOINTS
api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
api.add_resource(RegisterUser, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)