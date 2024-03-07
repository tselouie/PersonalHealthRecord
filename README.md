# Dockerized Python Server for a Personal Health Record keeping App
This repository contains a Dockerfile and a Python script (server.py) to run a RESTful server that performs **CRUD** operations in SQL for a NoteTaker. The server is built using _Python 3.10.9_ and is dockerized for portability.

[Github Repository Link](https://github.com/tselouie/PersonalHealthRecord)
### Directory Structure

| File          | Description                                           |
|---------------|-------------------------------------------------------|
| docker-compose.yml    | Defines the container for both db and application.              |
| Dockerfile    | Defines the Docker image for the server.              |
| server.py     | Contains the implementation of the HTTP server.       |
| .env.example  | Defines the structure for a .env file.                |
| .gitignore    | Defines what we want to avoid pushing to the repo.    |


### Setup 
#### Run Locally
Use this command to create a network
```bash
docker network create {NetworkName}
```

Use this command to create the database:

```bash
docker run --name {ContainerName} -p 3306:3306 -e MYSQL_ROOT_PASSWORD={Password} -e MYSQL_DATABASE={DatabaseName} -d mysql:latest
```
Remember the ContainerName,Password, and DatabaseName as we will use them for our environment variables.

Create `.env` file and use the values we used to create the database
```bash
DATABASE_URL=localhost
DATABASE_PASSWORD={Password}
DATABASE_NAME={DatabaseName}
```
Install dependencies for the code

```bash
pip install python-dotenv mysql-connector-python
or
python -m pip install python-dotenv mysql-connector-python
```

Run the server - 
*On first run, the server will create the tables and two dummy entries for each table.*
```bash
python server.py
```
#### Using Docker 

Create Docker files:
```bash 
touch docker-compose.yml
touch Dockerfile
```
Build our app using the settings in Dockerfile
```bash
docker build -t personal-health-record-system:version .
```
Once the image is built, you can run the Docker container using the following command:
```bash
docker run -dp 8010:8010 personal-health-record-system
```

Run this code to containerize the sql image and build the application images and create a compiled container of both systems all in one command:

```bash
docker-compose up
```
### Pushing to DockerHub
```bash
# Build the application
docker-compose build app

# Tag the build application with a name
docker tag personalhealthrecord-app lttse/personalhealthrecord-api:v1

# Push the image to DockerHub
docker push lttse/personalhealthrecord-api:v1
```

The HTTP server inside the container will start, and listen on port 8010. You can access the server at http://localhost:8010.

## Database
This project uses MySQL database from Docker.
| File          | Description                                           |
|---------------|-------------------------------------------------------|
| db_init.sql   | This defines the table creations along with two dummy users.    |
| db_seed.sql   | This file holds the insert statements for dummy data.              |
| db_setup.py   | This file holds the code to run the sql files to setup the database.     |

## API Testing Endpoints

- [Link to Documentation](https://documenter.getpostman.com/view/33019960/2sA2xfXYMX)
- [Link to Postman Workspace](https://www.postman.com/orange-desert-612142/workspace/phr/overview)
