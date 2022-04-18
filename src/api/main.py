import json
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends
import pika
import schemas
from db import SessionLocal
from db import Base, engine, Geography, City, Continent

app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

async def validate_data(data):
    print("Validate data")
    if data.continent_population < data.city_population:
        return False
    if data.continent_area < data.country_area:
        return False
    if data.continent_area < data.city_area:
        return False
    if data.country_area < data.city_area:
        return False
    return True

@app.get("/")
async def root():
    return {"message": "Hello Team Vector.ai"}

@app.post(
    "/geography", response_model=schemas.Geography, status_code=status.HTTP_201_CREATED
)
async def create_geography(geography: schemas.GeographyCreate):
    """
    Post method to create a record
    INPUT: Model of GeographyCreate
    OUTPUT: Continent name (We can use DB session here to depend on that)
    """
    try:
        print("create geography")
        ret = await validate_data(geography)
        if ret:
            print("Valid Data")
            session = SessionLocal()
            
            continent = session.query(Continent).filter(Continent.continent_name == geography.continent_name)
            con = continent.one_or_none()
            print(con.total_continent_population)
            print(geography.city_population)
            #TODO: Similarly we can do the below logic for area and population parameters
            if con.total_continent_population < geography.city_population:
                return "City population cannot be greater than Continent Population"
            # Connect to RabbitMQ using pika client and declare queue for insertion
            connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
            channel = connection.channel()
            channel.queue_declare(queue="insertion", durable=True)

            # prepare the json to insert and publish to the queue, return with continent name. Refer ResponseModel
            geo_db = {
                "continent_name": geography.continent_name,
                "country_name": geography.country_name,
                "city_name": geography.city_name,
                "continent_population": geography.continent_population,
                "city_population": geography.city_population,
                "continent_area": geography.continent_area,
                "country_area": geography.country_area,
                "city_area": geography.city_area,
                "city_num_roads": geography.city_num_roads,
                "city_num_trees": geography.city_num_trees,
                "country_num_hospitals": geography.country_num_hospitals,
                "country_num_parks": geography.country_num_parks,
            }
            channel.basic_publish(exchange="", routing_key="insertion", body=json.dumps(geo_db))
            connection.close()
            return geography
        return "Invalid Data"
    except Exception as ex:
        print(f"Expcetion in create_geography() {ex}")
        return HTTPException(status_code=500, detail=f"Something went wrong")

@app.put("/geography/{id}")
async def update_data(id: int, geography: Optional[schemas.GeographyUpdate]):
    '''
    PUT method to update the set of parameters
    INPUT: Set of parameters as in GeographyUpdate Model and ID
    OUTPUT: response string
    '''
    try:
        print("update data")
        ret = await validate_data(geography)
        if ret:
            session = SessionLocal()

            to_update = session.query(Geography).get(id)
            print(to_update)
            if to_update is not None:
                print("ID exists")
                # Connect to RabbitMQ using pika client and declare queue for updation
                connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
                channel = connection.channel()
                channel.queue_declare(queue="updation", durable=True)

                # prepare the json and publish to the queue
                geo_db = {
                    "id": id,
                    "continent_population": geography.continent_population,
                    "city_population": geography.city_population,
                    "city_num_roads": geography.city_num_roads,
                    "city_num_trees": geography.city_num_trees,
                    "country_num_hospitals": geography.country_num_hospitals,
                    "country_num_parks": geography.country_num_parks,
                }

                channel.basic_publish(exchange="", routing_key="updation", body=json.dumps(geo_db))
                connection.close()

            # check if item with given id exists. If not, raise exception and return 404 not found response
            else:
                print("ID does not exist")
                return HTTPException(status_code=404, detail=f"item with id {id} not found")

            return "Updated Successfully"
        else:
            return "Record is not updated"
    except Exception as ex:
        print(f"Exception in update method() {ex}")
        return HTTPException(status_code=500, detail=f"Something went wrong with {id}")

@app.delete("/geography/{id}")
async def delete_data(id: int):
    '''
    Delete method to delete the data based on the ID
    '''
    try:
        print("delete data")
        session = SessionLocal()
        to_delete = session.query(Geography).get(id)
        if to_delete:
            # Connect to RabbitMQ using pika client and declare queue for delettion
            connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
            channel = connection.channel()
            channel.queue_declare(queue="deletion", durable=True)
            channel.basic_publish(exchange="", routing_key="deletion", body = json.dumps(id))
            connection.close()
        else:
            return HTTPException(status_code=404, detail=f"item with id {id} not found")
        return "Deleted Successfully"
    except Exception as ex:
        print(f"Exception in delete method() {ex}")
        return HTTPException(status_code=500, detail=f"Something went wrong with id {id}")


