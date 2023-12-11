from kafka import KafkaConsumer
import json
from pymongo import MongoClient

bootstrap_servers = 'kafka:9092'
topic = 'tickets'

consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Connect to MongoDB
mongo_client = MongoClient("mongodb://root:example@mongo")
db = mongo_client["Commerce"]
tickets_collection = db["Tickets"]

try:
    for message in consumer:
        ticket_data = message.value
        print(f'Ticket consumed: {ticket_data}')

        # Save the ticket to MongoDB
        tickets_collection.insert_one(ticket_data)
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
    mongo_client.close()
