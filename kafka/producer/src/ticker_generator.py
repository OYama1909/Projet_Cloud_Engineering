from confluent_kafka import Producer
import json
import time

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Kafka topic to send tickets
ticket_topic = 'ticket_topic'

# Callback function to handle delivery reports from Kafka producer
def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Create Kafka producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers,
}

# Create Kafka producer instance
producer = Producer(producer_config)

# Example ticket data
ticket_data = {
    'store_id': 1,
    'cashier_id': 101,
    'product': 'item123',
    'quantity': 2,
    'price': 19.99,
    'timestamp': int(time.time())
}

# Convert ticket data to JSON format
ticket_json = json.dumps(ticket_data)

# Produce ticket to Kafka topic
producer.produce(ticket_topic, value=ticket_json, callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery reports received
producer.flush()
