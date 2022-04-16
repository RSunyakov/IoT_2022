from kafka import KafkaConsumer
import time

from kafka.consumer.fetcher import ConsumerRecord


class Consumer:
    def __init__(self):
        try:
            self.__consumer_instance = KafkaConsumer('api_messages', group_id='group_1', auto_offset_reset='earliest',
                                                     bootstrap_servers=['localhost:9092'], consumer_timeout_ms=1000)
        except Exception as e:
            print('Exception while connecting to Kafka')
            print(str(e))

    def consume(self):
        print(self.__consumer_instance)
        while True:
            message = self.__consumer_instance.poll(1.0)
            time.sleep(1)
            if not message:
                print('Waiting for a new messages...')
            else:
                for value in message.values():
                    record: ConsumerRecord = value[0]
                    sender_name = record.key.decode('utf-8')
                    text = record.value.decode('utf-8')
                    print('Received message from Kafka')
                    print(f'Sender: {sender_name}')
                    print(f'Text: {text}')


if __name__ == '__main__':
    c = Consumer()
    c.consume()
