#!/usr/bin/env python
import threading, logging, time
import os
from kafka import KafkaConsumer, KafkaProducer
import json
import redis

# Kafka Configurations
KAFKA_HOST_NAME = os.environ.get('KAFKA_HOST_NAME')
KAFKA_TOPIC_NAME = os.environ.get('KAFKA_TOPIC_NAME')

class Consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(KAFKA_TOPIC_NAME,bootstrap_servers=[KAFKA_HOST_NAME])
        consumer.subscribe([KAFKA_TOPIC_NAME])
        db = redis.Redis(host='redis',port=6379,db=0)

        for message in consumer:
            tweets=json.loads(message.value)
            for tag in tweets['entities']['hashtags']:
                print (tag['text'].lower())
                db.set('tw:'+tag['text'].lower(),tweets['text'])
                db.set('tw:'+tag['text'].lower()+":img",tweets['user']['profile_image_url'])
                db.incr(tag['text'].lower())

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
