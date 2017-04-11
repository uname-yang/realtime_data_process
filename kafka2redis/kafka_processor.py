#!/usr/bin/env python
import threading, logging, time

from kafka import KafkaConsumer, KafkaProducer

# Kafka Configurations
KAFKA_ENV_KAFKA_HOST_NAME = 'kafka'
KAFKA_TOPIC_NAME = os.environ.get('KAFKA_TOPIC_NAME')



class Consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(KAFKA_TOPIC_NAME,
                         bootstrap_servers=[KAFKA_ENV_KAFKA_HOST_NAME+":9092"])
        consumer.subscribe([KAFKA_TOPIC_NAME])

        for message in consumer:
            print (message)


def main():
    threads = [
        Consumer()
    ]

    for t in threads:
        t.start()

    time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()
