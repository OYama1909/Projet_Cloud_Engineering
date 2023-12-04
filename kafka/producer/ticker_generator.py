from flask import Flask, request, jsonify
from confluent_kafka import Producer

app = Flask(__name__)

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Kafka topic to produce tickets
ticket_topic = 'ticket_topic'

# Create Kafka producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers,
}

# Create Kafka producer instance
producer = Producer(producer_config)

@app.route('/', methods=['POST'])
def receive_ticket():
    ticket_data = request.data.decode('utf-8')

    # Produce the ticket to Kafka topic
    producer.produce(ticket_topic, value=ticket_data)
    producer.flush()

    return 'Ticket received and produced to Kafka\n'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
