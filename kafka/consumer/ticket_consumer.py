from confluent_kafka import Consumer, KafkaException
import json
from pymongo import MongoClient

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Kafka topic to consume tickets
ticket_topic = 'ticket_topic'

# MongoDB connection details
mongodb_host = 'localhost'
mongodb_port = 27017
mongodb_database = 'my_database'
mongodb_collection = 'tickets'

# Create Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest',
}

# Create Kafka consumer instance
consumer = Consumer(consumer_config)

# Subscribe to the ticket topic
consumer.subscribe([ticket_topic])

# Create MongoDB client and connect to the database
mongo_client = MongoClient(mongodb_host, mongodb_port)
db = mongo_client[mongodb_database]
collection = db[mongodb_collection]

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                print("Reached end of partition, resetting consumer position")
                consumer.seek(msg.partition(), msg.offset())
            else:
                print("Error: {}".format(msg.error()))
        else:
            # Process the consumed ticket
            ticket_data = json.loads(msg.value())
            print("Received Ticket: {}".format(ticket_data))

            # Save the ticket to MongoDB
            collection.insert_one(ticket_data)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
    mongo_client.close()
