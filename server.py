from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from dotenv import load_dotenv
import os
import mysql.connector
from db_setup import db_init 
from urllib.parse import urlparse, parse_qs
from datetime import date,datetime
load_dotenv();  # take environment variables from .env.
# function to connect to database
def db_connection():
    return mysql.connector.connect(
    host=os.environ.get("DATABASE_URL"),
    user="root",
    database=os.environ.get("DATABASE_NAME"),
    password=os.environ.get("DATABASE_PASSWORD"))

#helper function for dates
def parse_dates(obj):
    if isinstance(obj, (datetime, date)):
        return obj.strftime("%Y-%m-%d")  # Customize the format as needed
    elif isinstance(obj, dict):
        return {k: parse_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [parse_dates(item) for item in obj]
    else:
        return obj

class RequestHandler(BaseHTTPRequestHandler):

    # Fetch records from database
    def do_GET(self):
        parsed_path = urlparse(self.path)
        parameters = parse_qs(parsed_path.query)

        path_parts = parsed_path.path.split('/')[1:]  # Split path and remove the first empty string

        #if there are 2 parameters: (table and user_id)
        if len(path_parts) == 2 and path_parts[0] in ['users', 'healthrecords', 'medications', 'allergies', 'emergencycontacts']:
            
            # if parameter: health_info=true join all tables to user
            health_info = parameters.get("health_info",[None])[0]
            table, user_id = path_parts
            if health_info is not None:
                if health_info.lower() in ['true','1']:
                    # Get all table data associated with user_id
                    self.handle_user_query(user_id)
            else: 
                # Get data with table and related user_id
                self.handle_table_query(table, user_id)
                
        #if there is 1 parameter return all rows for that table
        elif len(path_parts) == 1 and path_parts[0]  in ['users', 'healthrecords', 'medications', 'allergies', 'emergencycontacts']:
            self.handle_table_query(path_parts[0])
        else:
            self.send_error(404, "Resource not found")

    # Use this function to fetch all the data from the database, user_id is optional if you want to fetch only 1
    def handle_table_query(self, table, user_id=None):
        db = db_connection()
        cursor = db.cursor(dictionary=True)
        parsed_tablename = table[0].upper() + table[1:] if table else table
        if user_id == None:
            query = f"SELECT * FROM {parsed_tablename}"
            cursor.execute(query)

        else:
            query = f"SELECT * FROM {parsed_tablename} WHERE UserID = %s"
            cursor.execute(query, (user_id,))

        rows = cursor.fetchall()
   
        rows = parse_dates(rows)

        cursor.close()
        db.close()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(rows).encode())
    
    def handle_user_query(self, user_id):
        db = db_connection()
        cursor = db.cursor(dictionary=True)

       # Prepare the response structure
        user_profile = {
            "UserInfo": None,
            "HealthRecords": [],
            "Medications": [],
            "Allergies": [],
            "EmergencyContacts": []
        }

        # Fetch user info
        cursor.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
        user_info = cursor.fetchone()
        user_profile['UserInfo'] = user_info

        # Fetch health records
        cursor.execute("SELECT * FROM Healthrecords WHERE UserID = %s", (user_id,))
        health_records = cursor.fetchall()
        user_profile['HealthRecords'] = health_records

        # Fetch medications
        cursor.execute("SELECT * FROM Medications WHERE UserID = %s", (user_id,))
        medications = cursor.fetchall()
        user_profile['Medications'] = medications

        # Fetch allergies
        cursor.execute("SELECT * FROM Allergies WHERE UserID = %s", (user_id,))
        allergies = cursor.fetchall()
        user_profile['Allergies'] = allergies

        # Fetch emergency contacts
        cursor.execute("SELECT * FROM Emergencycontacts WHERE UserID = %s", (user_id,))
        emergency_contacts = cursor.fetchall()
        user_profile['EmergencyContacts'] = emergency_contacts

        user_profile = parse_dates(user_profile)
        cursor.close()
        db.close()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(user_profile).encode())
        
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]  # Split path and remove the first empty string
        # Get the size of the data
        content_length = int(self.headers['Content-Length'])
        # Read the body of the POST request
        post_data = self.rfile.read(content_length)
        #if there are 2 parameters find rows by table and user
        if len(path_parts) == 2 and path_parts[0] in ['users', 'healthrecords', 'medications', 'allergies', 'emergencycontacts']:
            table, action = path_parts
            if action == "create": 
                if self.handle_create_row(table,post_data):
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Data inserted successfully")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Error inserting data")

    def handle_create_row(self, table, data):
        db = db_connection()
        cursor = db.cursor(dictionary=True)
        data_str = data.decode('utf-8')
        data = json.loads(data_str)

        if table == "users":
            query = "INSERT INTO Users (Username, PasswordHash, Email, FullName, DateOfBirth, Gender, Active) VALUES (%s, %s, %s, %s, %s, %s,1)"
            values = (data['Username'], data['PasswordHash'], data['Email'], data['FullName'], data['DateOfBirth'], data['Gender'])

        elif table == "healthrecords":
            query = "INSERT INTO Healthrecords (UserID, RecordType, RecordDate, Description, ProviderName) VALUES (%s, %s, %s, %s, %s)"
            values = (data['UserID'], data['RecordType'], data['RecordDate'], data['Description'], data['ProviderName'])

        elif table == "medications":
            query = "INSERT INTO Medications (UserID, MedicationName, Dosage, StartDate, EndDate, Reason) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (data['UserID'], data['MedicationName'], data['Dosage'], data['StartDate'], data['EndDate'], data['Reason'])

        elif table == "allergies":
            query = "INSERT INTO Allergies (UserID, Allergen, Reaction, Severity) VALUES (%s, %s, %s, %s)"
            values = (data['UserID'], data['Allergen'], data['Reaction'], data['Severity'])

        elif table == "emergencycontacts":
            query = "INSERT INTO Emergencycontacts (UserID, FullName, Relationship, Phone, Email) VALUES (%s, %s, %s, %s, %s)"
            values = (data['UserID'], data['FullName'], data['Relationship'], data['Phone'], data['Email'])

        else:
            db.close()  # Ensure the connection is closed in case of an invalid table
            return False

        cursor.execute(query, values)
        db.commit()
        cursor.close()
        db.close()
        return True
    
    # Post method that update a record with id, title and content values in body object
    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]  # Split path and remove the first empty string
        
        # Expecting the URL format to be /{table}/{id} for the PUT request
        if len(path_parts) == 2 and path_parts[0] in ['users', 'healthrecords', 'medications', 'allergies', 'emergencycontacts']:
            table, record_id = path_parts
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            
            if self.handle_update_row(table, record_id, put_data):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Data updated successfully")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error updating data")

    def handle_update_row(self, table, id, data):
        db = db_connection()
        cursor = db.cursor(dictionary=True)
        data_str = data.decode('utf-8')
        data = json.loads(data_str)

        # Construct the SQL query and values based on the table
        if table == "users":
            query = "UPDATE Users SET Username = %s, PasswordHash = %s, Email = %s, FullName = %s, DateOfBirth = %s, Gender = %s WHERE ID = %s"
            values = (data['Username'], data['PasswordHash'], data['Email'], data['FullName'], data['DateOfBirth'], data['Gender'], id)

        elif table == "healthrecords":
            query = "UPDATE Healthrecords SET UserID = %s, RecordType = %s, RecordDate = %s, Description = %s, ProviderName = %s WHERE ID = %s"
            values = (data['UserID'], data['RecordType'], data['RecordDate'], data['Description'], data['ProviderName'], id)

        elif table == "medications":
            query = "UPDATE Medications SET UserID = %s, MedicationName = %s, Dosage = %s, StartDate = %s, EndDate = %s, Reason = %s WHERE ID = %s"
            values = (data['UserID'], data['MedicationName'], data['Dosage'], data['StartDate'], data['EndDate'], data['Reason'], id)

        elif table == "allergies":
            query = "UPDATE Allergies SET UserID = %s, Allergen = %s, Reaction = %s, Severity = %s WHERE ID = %s"
            values = (data['UserID'], data['Allergen'], data['Reaction'], data['Severity'], id)

        elif table == "emergencycontacts":
            query = "UPDATE Emergencycontacts SET UserID = %s, FullName = %s, Relationship = %s, Phone = %s, Email = %s WHERE ID = %s"
            values = (data['UserID'], data['FullName'], data['Relationship'], data['Phone'], data['Email'], id)

        else:
            db.close()  # Ensure the connection is closed in case of an invalid table
            return False

        try:
            cursor.execute(query, values)
            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return False
        finally:
            cursor.close()
            db.close()

        return True
    # Delete method that deletes a record provided 'id' in body object

    def handle_delete_row(self,table,id):
        db = db_connection()
        cursor = db.cursor()
        parsed_tablename = table[0].upper() + table[1:] if table else table
        query = f"DELETE FROM {parsed_tablename} WHERE ID = %s"
        cursor.execute(query, (id,))
        db.commit()
        db.close()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"{table} {id} deleted".encode())

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.split('/')[1:]  # Split path and remove the first empty string

        if len(path_parts) != 2:
            self.send_error(400, "URL must be in the format /table_name/id")
            return
        
        table, id = path_parts
        try:
            self.handle_delete_row(table, int(id))  # Assuming ID is an integer
        except ValueError:  # In case the ID is not an integer
            self.send_error(400, "ID must be an integer")
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")

def run(serverClass=HTTPServer,handlerClass=RequestHandler,port=8010):
    db_init() # create all tables and initial records
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