from kafka import KafkaProducer


class Producer:
    def __init__(self):
        try:
            self.__producer_instance = KafkaProducer(bootstrap_servers=['localhost:9092'])
        except Exception as e:
            print('Exception while connecting to Kafka')
            print(str(e))

    def produce(self, sender_name: str, text: str):
        try:
            sender_name_bytes = bytes(sender_name, encoding='utf-8')
            text_bytes = bytes(text, encoding='utf-8')
            self.__producer_instance.send(topic='api_messages', key=sender_name_bytes, value=text_bytes)
            return 'Message has been sent successfully'
        except Exception as e:
            print(e)
            return 'Exception while sending message to Kafka topic'
