from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='kafka:9092')

producer.send('foobar', b'some_message_bytes')

producer.flush()
