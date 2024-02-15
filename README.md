# Dockerized Python Server for Toronto Time
This repository contains a Dockerfile and a Python script (server.py) to run a RESTful server that performs
CRUD operations in SQL for a NoteTaker. The server is built using Python 3.11 and is dockerized for easy deployment.

### Setup

Use this command to create the database:

`docker run --name {ContainerName} -p
3306:3306 -e MYSQL_ROOT_PASSWORD={Password} -e MYSQL_DATABASE={DatabaseName} -d mysql:latest`

pip install python-dotenv
pip install mysql-connector-python













To build and run the Docker container:
Ensure you have Docker installed on your system.
Clone this repository to your local machine.
Navigate to the root directory of the repository.
Building the Docker Image
To build the Docker image, run the following command:

```bash
docker build -t toronto-time-server .
```
##### Running the Docker Container
Once the image is built, you can run the Docker container using the following command:
```bash
docker run -d -p 8010:8010 toronto-time-server
```
This will start the HTTP server inside the container, listening on port 8010. You can access the server at http://localhost:8010.

Usage
Once the server is running, you can send GET requests to http://localhost:8010 to retrieve the current time in Toronto in JSON format.

##### Example request:
```bash
curl http://localhost:8010
```
##### Example response:

```json
{
  "TorontoTime": "2024-02-15 12:00:00"
}
```

#### Server Implementation Details
The server is implemented using Python's built-in http.server module. It creates a simple HTTP server that handles GET requests by returning the current time in Toronto timezone as JSON.

The logic for calculating the Toronto time is done by subtracting 5 hours from the current UTC time.

#### Directory Structure
Dockerfile: *Defines the Docker image for the server.*
server.py: *Contains the implementation of the HTTP server.*
README.md: *This file.*

#### Contributions
Contributions to improve or extend this project are welcome! If you encounter any issues or have suggestions for enhancements, please feel free to open an issue or submit a pull request.

##### License
This project is licensed under the MIT License.