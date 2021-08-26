# import sqlite3
from db import db

class UserModel(db.Model):
    
    # tell sql-alchemy the table name
    __tablename__ = 'users'
    # Columns the table contains
    id = db.Column(db.Integer, primary_key=True) # creates auto incrementing id field
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))



    def __init__(self, username, password):
        self.username = username
        self.password = password 

    def save_to_db(self):
        # to remove from session => db.session.delete(self)
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query, (username,)) # always in form of tuple
        # row = result.fetchone() # get first row out of result set, if no rows -> None
        # if row:
        #     # user = cls(row[0], row[1], row[2]) 
        #     user = cls(*row) # id, username, password
        # else:
        #     user = None

        # connection.close()
        # return user

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query, (_id,)) # always in form of tuple
        # row = result.fetchone() # get first row out of result set, if no rows -> None
        # if row:
        #     # user = cls(row[0], row[1], row[2]) 
        #     user = cls(*row) # id, username, password
        # else:
        #     user = None

        # connection.close()
        # return user