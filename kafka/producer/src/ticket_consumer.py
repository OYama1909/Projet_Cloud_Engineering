from confluent_kafka import Consumer, KafkaException
import json

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Kafka topic to consume tickets
ticket_topic = 'ticket_topic'

# Create Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest',  # Start reading from the beginning of the topic
}

# Create Kafka consumer instance
consumer = Consumer(consumer_config)

# Subscribe to the ticket topic
consumer.subscribe([ticket_topic])

try:
    while True:
        # Poll for messages from Kafka broker
        msg = consumer.poll(1.0)  # Timeout set to 1 second

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                # End of partition event
                print("Reached end of partition, resetting consumer position")
                consumer.seek(msg.partition(), msg.offset())
            else:
                print("Error: {}".format(msg.error()))
        else:
            # Process the consumed ticket
            ticket_data = json.loads(msg.value())
            print("Received Ticket: {}".format(ticket_data))

except KeyboardInterrupt:
    pass
finally:
    # Close down consumer to commit final offsets.
    consumer.close()
