import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv();  # take environment variables from .env.

def db_connection():
    return mysql.connector.connect(
    host=os.environ.get("DATABASE_URL"),
    user="root",
    database=os.environ.get("DATABASE_NAME"),
    password=os.environ.get("DATABASE_PASSWORD"))

def db_init():

    try:
        # Connect to the MySQL database
            # Database connection parameters
        conn = db_connection()
        cursor = conn.cursor()

        # Open and read the SQL file
        with open('db_init.sql', 'r') as file:
            sql_commands = file.read().split(';')  # Split by ';' to separate commands

        # Execute each SQL command
        for command in sql_commands:
            if command.strip():  # Checking if command is not empty
                cursor.execute(command)
        
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    db_init()
