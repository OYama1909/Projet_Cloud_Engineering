from kafka import KafkaProducer
import json
import schedule
import time
from random import choice

bootstrap_servers = 'kafka:9092'
topic = 'tickets'

producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

store_id = 1  # Replace with the actual store ID

def generate_ticket():
    # Simulate ticket generation
    ticket_data = {
        "store_id": store_id,
        "product": choice(["Apple", "Orange", "Bottle of water"]),
        "quantity": 1,
        "price": 0  # You can calculate the total price based on product and quantity
    }

    producer.send(topic, value=ticket_data)
    print(f'Ticket produced: {ticket_data}')

# Schedule the ticket generation every 1 second
schedule.every(1).seconds.do(generate_ticket)

while True:
    schedule.run_pending()
    time.sleep(1)
