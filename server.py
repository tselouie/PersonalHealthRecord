from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from dotenv import load_dotenv
import os
import mysql.connector
load_dotenv();  # take environment variables from .env.
host=os.environ.get("DATABASE_URL")

def db_connection():
    return mysql.connector.connect(
    host=os.environ.get("DATABASE_URL"),
    user="root",
    database=os.environ.get("DATABASE_NAME"),
    password=os.environ.get("DATABASE_PASSWORD"))

def db_init():
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL
        )
    """)
    db.commit()
    print("Database initialized with notes table.")
    db.close()
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        db = db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notes")
        notes = cursor.fetchall()
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.end_headers()
        message = json.dumps({
            'data':notes
        })
        self.wfile.write(message.encode('utf-8'))
        
    def do_POST(self):
        if self.path == '/create': 
            db = db_connection()
            cursor = db.cursor()
            # create note
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            print(post_data)
            cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)",(post_data['title'],post_data['content']))
            db.commit()
            self.send_response(200)
            self.end_headers()
            message = json.dumps({
                'message':"Note created successfully!"
            })
            self.wfile.write(message.encode('utf-8'))

    def do_PUT(self):
        if self.path == '/update':
            db = db_connection()
            cursor = db.cursor()
            content_length = int(self.headers['Content-Length'])
            put_data = json.loads(self.rfile.read(content_length))
            cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s",(put_data["title"],put_data["content"],put_data["id"]))
            db.commit()
            self.send_response(200)
            self.end_headers()
            message = json.dumps({
                'message':"Note updated successfully!"
            })
            self.wfile.write(message.encode('utf-8'))
    def do_DELETE(self):
        if self.path == '/delete':
            db = db_connection()
            cursor = db.cursor()
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            cursor.execute("DELETE FROM notes WHERE id = %s",(post_data["id"],))
            db.commit()
            self.send_response(200)
            self.end_headers()
            message = json.dumps({
                'message':"Note deleted successfully!"
            })
            self.wfile.write(message.encode('utf-8'))

def run(serverClass=HTTPServer,handlerClass=RequestHandler,port=8010):
    db_init() # create notes table
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