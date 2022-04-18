import json
import pika, sys, os
from database import SessionLocal
from database import Base, engine
import models

# Create the database table
Base.metadata.create_all(engine)

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def main():
    """
    Main function to create the pika client of RabbitMQ
    Declare the queues and callback function which will be hit on consuming the data on the queue
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672))
        channel = connection.channel()

        channel.queue_declare(queue="insertion", durable=True)
        channel.queue_declare(queue="updation", durable=True)
        channel.queue_declare(queue="deletion", durable=True)

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            print(json.loads(body))
            insert_data(json.loads(body))

        def update_callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            print(json.loads(body))
            update_data(json.loads(body))
        
        def delete_callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            print(json.loads(body))
            delete_data(json.loads(body))

        channel.basic_consume(
            queue="insertion", on_message_callback=callback, auto_ack=True
        )
        channel.basic_consume(
            queue="updation", on_message_callback=update_callback, auto_ack=True
        )
        channel.basic_consume(
            queue="deletion", on_message_callback=delete_callback, auto_ack=True
        )

        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as ex:
        print(f"Exception in main method() {ex}")
        print(ex)
        # main()

def insert_data(geography):
    """
    When the insertion queue receives the data, insert to the DB
    INPUT: geography dict
    """
    try:
        geo_db = models.Geography(
            continent_name=geography["continent_name"],
            country_name=geography["country_name"],
            city_name=geography["city_name"],
            continent_population=geography["continent_population"],
            city_population=geography["city_population"],
            continent_area=geography["continent_area"],
            country_area=geography["country_area"],
            city_area=geography["city_area"],
            city_num_roads=geography["city_num_roads"],
            city_num_trees=geography["city_num_trees"],
            country_num_hospitals=geography["country_num_hospitals"],
            country_num_parks=geography["country_num_parks"],
        )
        session = SessionLocal()
        continent = session.query(models.Continent).filter(models.Continent.continent_name == geography["continent_name"])
        total_conti = geography["continent_population"]
        con = continent.one_or_none()
        if con == None:
            con = models.Continent(
            continent_name=geography["continent_name"],
            total_continent_population=total_conti
        )
        else:            
            total_conti = con.total_continent_population + geography["continent_population"]
            con.total_continent_population = total_conti
        

        city = session.query(models.City).filter(models.City.city_name == geography["city_name"])
        total_city = geography["city_population"]
        city_c = city.one_or_none()
        if city_c == None:
            city_c = models.City(
            city_name=geography["city_name"],
            total_city_population=total_city
        )
        else:            
            total_city = city_c.total_city_population + geography["city_population"]
            city_c.total_city_population = total_city

        # add it to the session and commit it
        session.add(con)
        session.add(geo_db)
        session.add(city_c)
        session.commit()
        print("To be refresh")
        session.refresh(geo_db)
        session.refresh(con)
        session.refresh(city_c)
        print("refreshed")

        # close the session
        session.close()
    except Exception as ex:
        print(f"Exception in insert data {ex}")

def update_data(geography):
    """
    When the updation queue receives the data, update to the DB
    INPUT: geography dict
    NOTE: deleting the data whose values are 0. Assuming 0 means not to update in this case
    """
    try:
        session = SessionLocal()
        to_update = session.query(models.Geography).get(geography["id"])
        for key, value in list(geography.items()):
            if value == 0:
                del geography[key]
        for key, value in geography.items():
            if key == "id":
                continue
            setattr(to_update, key, value)
        session.commit()
        session.close()
    except Exception as ex:
        print(f"Exception in update data {ex}")

def delete_data(id):
    try:
        session = SessionLocal()
        to_delete = session.query(models.Geography).get(id)

        # if to_delete item with given id exists, delete it from the database. Otherwise raise 404 error
        if to_delete:
            session.delete(to_delete)
            session.commit()
            session.close()
    except Exception as ex:
        print(f"Exception in delete data {ex}")
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
