from models.user import UserModel
# import sqlite3
from flask_restful import Resource, reqparse
    
class RegisterUser(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be nil")
    parser.add_argument('password', type=str, required=True, help="This field cannot be nil")
    
    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"A user '{data['username']}' already exists"}, 400

        user = UserModel(data['username'], data['password']) # or UserModel(**data)
        user.save_to_db()


        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO users VALUES (NULL, ?, ?)" # no id => primary key auto increment
        # cursor.execute(query, (data['username'], data['password']))

        # connection.commit()
        # connection.close()

        return {"message": "User created (:"}, 201