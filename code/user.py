import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password 
    
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,)) # always in form of tuple
        row = result.fetchone() # get first row out of result set, if no rows -> None
        if row:
            # user = cls(row[0], row[1], row[2]) 
            user = cls(*row) # id, username, password
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,)) # always in form of tuple
        row = result.fetchone() # get first row out of result set, if no rows -> None
        if row:
            # user = cls(row[0], row[1], row[2]) 
            user = cls(*row) # id, username, password
        else:
            user = None

        connection.close()
        return user
    
class RegisterUser(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be nil")
    parser.add_argument('password', type=str, required=True, help="This field cannot be nil")
    
    def post(self):
        data = RegisterUser.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": f"A user '{data['username']}' already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)" # no id => primary key auto increment
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created (:"}, 201