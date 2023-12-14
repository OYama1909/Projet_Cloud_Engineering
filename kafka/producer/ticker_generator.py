from random import randint, sample, choice
from kafka import KafkaProducer
import json
import schedule
import time

bootstrap_servers = 'kafka:9092'
topic = 'tickets'

producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

store_id = 1  # Replace with the actual store ID

def generate_ticket():
    # Simulate ticket generation
    store_id = randint(1, 100)
    checkout_id = randint(1, 1000)
    seller_id = randint(1, 1200)
    basket = {product_name: randint(1, 5) for product_name in sample(["Apple", "Orange", "Milk", "Bottle of water"], randint(1, 4))}    
    ticket_data = {"store_id": store_id, "checkout_id": checkout_id, "seller_id": seller_id, "basket": basket, "total_price": sum(product_prices[product_name]*quantity for product_name, quantity in basket.items())}
    producer.send(topic, value=ticket_data)
    print(f'Ticket produced: {ticket_data}')

# Schedule the ticket generation every 1 second
schedule.every(1).seconds.do(generate_ticket)

while True:
    schedule.run_pending()
    time.sleep(1)
