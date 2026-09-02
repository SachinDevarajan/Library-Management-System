import mysql.connector
from config.confiq import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from config.schema import create_tables

try:
    # Connect to the MySQL server 
    server_connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    server_cursor = server_connection.cursor()
    server_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    server_connection.commit()
    server_cursor.close()
    server_connection.close()
except Exception as e:
    print("Error creating database :", e)
    raise

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
except Exception as e:
    print("Error connecting to database :", e)
    raise

# Create tables automatically
create_tables(connection, cursor)
