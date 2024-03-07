# base image is using the version of python you compiled with
FROM python:3.10.9

# specify working directory
WORKDIR /app

# copy out folder into /app
COPY . /app

# Install dependencies
RUN pip install python-dotenv mysql-connector-python requests bcrypt

ENV DATABASE_URL=host.docker.internal
#Expose the application port used in server.py
EXPOSE 8010

#Run the python server which will persist the RESTful API
CMD ["python", "server.py"]
