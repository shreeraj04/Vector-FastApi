# Vector.AI Assignment

A simple application with Create, Update and Delete APIs. All the requests are added to the message broker like RabbitMQ which in-turn talks to the database

# Technologies Used
 - FastAPI framework
 - RabbitMQ message broker
 - SQLAlchemy ORM
 - Python
 - SQLite

## How to deploy ?
I've created a Dockerfile for 2 services i.e api and worker. API is a FastAPI solution whereas worker is handling the message queues from api. Therefore these two acts as a microservice architecture. One more service is rabbitmq.

To run API in local - [from api folder]

    uvicorn main:app --reload

To run worker in local - [from worker folder]

    python worker.py
To run rabbitmq [docker]

    docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 --network myNetwork rabbitmq:3-management

> rabbitmq:3-management is the docker image being used here.

We can run altogether the services using docker-compose also. 
*[Not working in this assignment]*

    sudo docker load --input rabbitmq.tar.gz
    sudo docker load --input assignment_api.tar.gz
    sudo docker load --input assignment_worker.tar.gz
    sudo docker-compose up -d --no-build

## Features Developed
There are three APIs in total.

 - Create Geography - In this POST Api, a set of request payload is sent which is added to the 'insertion' rabbitmq. The queue then inserts the data to the SQLite database
 - Update Geography - In this PUT Api, a set of request to be updated with ID is sent which is added to the 'updation' rabbitmq. The queue then checks the values of all the keys which are 0. Those keys are removed from the dictionary assuming that the client doesn't want to update that. The rest of the data is updated for the ID
 - Delete Geography - In this DELETE Api, an ID is sent which is added to the 'deletion' rabbitmq. The queue then checks if the ID exists or not, if exists that record will be deleted from the database.
 - Worker service is fully responsible to handle the different queues and do the task for the API. This is been implemented using RabbitMQ message broker. Here, we can also use Redis Pub/Sub, Kafka etc.,
 - SQLAlchemy ORM is being used here, on start of the worker a database table will be created if not present in an SQLite file. SQLite is a file system kind of database. Any other relational database also can be used instead of SQLite like MSSQL, Postgres, MySQL etc.,
 - FastAPI provides the Swagger docs for the client to check the API details and payload details
 - I've chosen RabbitMQ because I actually found it useful to use than kafka.
 - In Create API - I am checking if the continent and city name is already present or not. If present, updating the total count in a seperate table
 - In Create API - Checking few validations from the total count table for continent population and city population (area wise as well)

## Pending from Assignment

 - Validation check before adding or updating to the database.
	 - How it can be done ?
		 - We can make a proper DB design and table structure with relationships between the table. Currently there are 3 tables - Geography, City and Continent.
		 We can have a proper design with relationship between the continent, country and city data.
		 - During update, we can check if the 'count columns' for a particular continent or country is lesser than the new value or not. If not satisfied, we can let the client know about the information.
 -   Running from docker is working, but the APIs aren't working in a docker environment.

## Production Deployment
* Docker is a production ready system which is used nowadays in everywhere in an IT organization for the deployment.
* As this solution has 3 microservice - api, worker and rabbitmq, we can use docker-compose to run the 3 docker containers.

### Note
* I used FastAPI as I got to know that you guys are using it. I was actually knowing flask, aiohttp and gunicorn only. For this assignment I went through the fastapi docs and developed this
* I have never using any message broker till now. I have only worked on Redis, pub/sub itself. For this assignment, went through RabbitMQ and implemented in this assignment
* Maybe, there are many other techniques to use or implement both of these than how I have done here. I feel I will get to know and explore more when I actually work with real world projects in your organization or anywhere who are actually using it on a daily basis.
* Number of hours totally spent on *development, documentation and understanding fastapi, rabbitmq*: **Approx. 16.5 hours**
