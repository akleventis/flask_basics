import sqlite3

# initialize connection
connection = sqlite3.connect('data.db')

# responsible for query/store db queries
cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
select_query = "SELECT * FROM users"

# run query
cursor.execute(create_table)


# for single -> cursor.execute(insert_query, user)
# for multiple -> cursor.executemany(insert_query, {list of tuples})
users = [
    (1, 'finnthehuman', '123'),
    (2, 'jakethedog', '456')
]
cursor.executemany(insert_query, users)

for row in cursor.execute(select_query):
    print(row)

# save db changes
connection.commit()

# close db connection
connection.close()