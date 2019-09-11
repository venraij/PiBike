#!/usr/bin/python3

# import connection module; name it mariadb
import mysql.connector as mariadb
import json;

# initialize
data = []

# connect to the database
mariadb_connection = mariadb.connect(
    user='senser',
    password='h@',
    database='pibike')

# create a cursor object for executing queries
cursor = mariadb_connection.cursor()

stmt = 'SELECT sensor_id, waarde FROM meting WHERE sensor_id = 1 OR sensor_id = 2 ORDER BY id DESC LIMIT 2;'

cursor.execute(stmt)

num_fields = len(cursor.description)
field_names = [i[0] for i in cursor.description]

# returned rows (tuples)
rows = cursor.fetchall()

# close cursor and database
cursor.close()
mariadb_connection.close()

output_json = []
for row in rows:
    output_json.append(dict(zip(field_names,row)))

print("Content-type: application/json\n")
print(json.dumps(output_json))
# done
