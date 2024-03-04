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

def check_database_initialized(cursor):
    # Check if the database is already initialized
    # This can be checking for a specific table's existence, for example
    try:
        cursor.execute("SELECT * FROM Users LIMIT 1;")
        # If the above command doesn't throw an error, the table (and hence the DB) exists
        return True
    except mysql.connector.Error:
        # If an error is thrown, the table doesn't exist, and likely the DB is not initialized
        return False

def db_init():
    
    try:
        # Connect to the MySQL database
            # Database connection parameters
        conn = db_connection()
        cursor = conn.cursor()
        if not check_database_initialized(cursor):  

            # Open and read the SQL file
            with open('db_init.sql', 'r') as file:
                sql_commands = file.read().split(';')  # Split by ';' to separate commands

            # Create all the tables along with initial users
            for command in sql_commands:
                if command.strip():  # Checking if command is not empty
                    cursor.execute(command)

            # Insert Seeded data that have relations to users
            with open('db_seed.sql', 'r') as seed_file:
                seed_data_commands = seed_file.read().split(';') 
            for insert_query in seed_data_commands:
                if insert_query.strip():  
                    cursor.execute(insert_query)
            conn.commit()
            print("Database initialized and seeded.")
        else:
            print("Database already initialized. Skipping seeding.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    # finally:
    #     if conn.is_connected():
    #         cursor.close()
    #         conn.close()

if __name__ == '__main__':
    db_init()
