# Dockerized Python Server for a Note taking App
This repository contains a Dockerfile and a Python script (server.py) to run a RESTful server that performs **CRUD** operations in SQL for a NoteTaker. The server is built using Python 3.11 and is dockerized for portability.

### Setup
Use this command to create a network
```bash
docker network create {NetworkName}
```

Use this command to create the database:

```bash
docker run --name {ContainerName} -p 3306:3306 -e MYSQL_ROOT_PASSWORD={Password} -e MYSQL_DATABASE={DatabaseName} -d mysql:latest
```

Install dependencies for the code

```bash
pip install python-dotenv mysql-connector-python
or
python -m pip install python-dotenv mysql-connector-python
```

#### Environment Variables
DATABASE_URL must be: ```host.docker.internal``` when app is hosted in container, otherwise localhost will work.



#### Using Docker 

Create Docker files:
```bash 
touch docker-compose.yml
touch Dockerfile
```
Build our app using the settings in Dockerfile
```bash
docker build -t note-taker:version .
```
Once the image is built, you can run the Docker container using the following command:
```bash
docker run -dp 8010:8010 note-taker
```



Run this code to containerize the sql and notetaker images from Docker:
```bash
docker-compose up
```


#### Server Implementation Details
The server is implemented using Python's built-in http.server module. It creates a simple HTTP server that handles GET requests by returning the current time in Toronto timezone as JSON.


#### Directory Structure

| File          | Description                                           |
|---------------|-------------------------------------------------------|
| Dockerfile    | Defines the Docker image for the server.              |
| server.py     | Contains the implementation of the HTTP server.       |
| .env.example  | Defines the structure for a .env file.                |
| .gitignore    | Defines what we want to avoid pushing to the repo.    |


### API Testing Endpoints

This will start the HTTP server inside the container, listening on port 8010. You can access the server at http://localhost:8010.

Usage
Once the server is running, you can send requests to http://localhost:8010 to interact with the notetaker database and receive data in JSON format.

##### Example request:
**GET**: List All Notes
**Description**: Retrieve a list of all notes.
**Endpoint**: /
**Method**: GET
**Headers**: Content_type: application/json
**Success Response**: 200 OK
```json
[
  {
    "id": "1",
    "title": "Hello",
    "content": "Time to code!",
  },
  {
    "id": "2",
    "title": "To-Do",
    "content": "Call plumber, Renew car insurance",
  }
]
```

**POST**: Create a New Note
**Description**: Create a new note.
**Endpoint**: /create
**Method**: POST
**Headers**: 
- Content_type: application/json
**Body**:
```json
{
  "title": "Title",
  "content": "description"
}
```
**Success Response**: 200 OK
```json
{"message": "Note created successfully!"}
```

**PUT**: Update a Note
**Description**: Update a note given the id and new values of the entry in JSON format.
**Endpoint**: /update
**Method**: PUT
**Headers**: 
- Content_type: application/json
**Body**:
```json
{
  "id":"id of note",
  "title": "Title",
  "content": "description"
}
```
**Success Response**: 200 OK
```json
{"message": "Note updated successfully!"}
```

**DELETE**: Delete a Note
**Description**: Delete note given the id.
**Endpoint**: /delete
**Method**: DELETE
**Headers**: 
- Content_type: application/json
**Body**:
```json
{
  "id":"id of note to delete",
}
```
**Success Response**: 200 OK
```json
{"message": "Note deleted successfully!"}
```

##### License
This project is licensed under the MIT License.