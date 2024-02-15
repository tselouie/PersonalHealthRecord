# base image is using the version of python you compiled with
FROM python:3.12.1

# specify working directory
WORKDIR /app

# copy out folder into /app
COPY . /app

#Expose the application port used in server.py
EXPOSE 8010

#Run the python server which will return the current toronto time as json for GET requests
CMD ["python", "server.py"]
