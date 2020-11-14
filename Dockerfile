#
# Docker file for GoOutSafe S4 v1.0
#
FROM python:rc-buster
LABEL maintainer="GoOutSafe Squad 4"
LABEL version="1.0"
LABEL description="Go Out Safe Application Squad 4"

# install gcc for ujson, psycopg2 for Postgres DB
RUN apt-get update && apt-get install -y libpq-dev gcc

# creating the environment
WORKDIR /app
COPY . /app

# installing all requirements
RUN ["pip", "install", "-r", "requirements.prod.txt"]

# removing gcc
RUN apt-get autoremove -y gcc

# exposing the port
EXPOSE 5000/tcp

# Main command
CMD ["flask", "run"]