import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# auto increment id primary key
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)" 
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)" # real = float
cursor.execute(create_table)


connection.commit()
connection.close()