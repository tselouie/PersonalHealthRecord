from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from dotenv import load_dotenv
import os
import mysql.connector
from db_setup import db_init 
from urllib.parse import urlparse, parse_qs
load_dotenv();  # take environment variables from .env.
# function to connect to database
def db_connection():
    return mysql.connector.connect(
    host=os.environ.get("DATABASE_URL"),
    user="root",
    database=os.environ.get("DATABASE_NAME"),
    password=os.environ.get("DATABASE_PASSWORD"))
# Create a table if it does not exist

class RequestHandler(BaseHTTPRequestHandler):

        
    # Get method that fetches all the notes from the database
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]  # Split path and remove the first empty string
        #if there are 2 parameters find rows by table and user
        if len(path_parts) == 2 and path_parts[0] in ['users', 'healthrecords', 'medications', 'allergies', 'emergencycontacts']:
            table, user_id = path_parts
            self.handle_table_query(table, user_id)
        #if there are 1 parameter return all rows for that table
        elif len(path_parts) == 1  in ['users', 'healthrecords', 'medications', 'allergies', 'emergencycontacts']:
            self.handle_table_query(table)
        else:
            self.send_error(404, "Resource not found")

    # Use this function to fetch all the data from the database, user_id is optional if you want to fetch only 1
    def handle_table_query(self, table, user_id=None):
        db = db_connection()
        cursor = db.cursor(dictionary=True)
        if user_id == None:
            query = f"SELECT * FROM {table}"
            cursor.execute(query)
        else:
            query = f"SELECT * FROM {table} WHERE UserID = %s"
            cursor.execute(query, (user_id,))

        rows = cursor.fetchall()
        db.close()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(rows).encode())
        
    def do_POST(self):
        pass
    # Post method that update a note with id, title and content values in body object
    def do_PUT(self):
        pass
    # Delete method that deletes a note provided 'id' in body object
    def do_DELETE(self):
        pass

def run(serverClass=HTTPServer,handlerClass=RequestHandler,port=8010):
    db_init() # create all tables and initial dataf
    serverAddress = ('',port)
    httpd = HTTPServer(serverAddress,RequestHandler)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping the httpd server..')

if __name__ == '__main__':
    run()