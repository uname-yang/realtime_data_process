#!/usr/bin/env python
from __future__ import absolute_import, print_function
import os
from kafka import KafkaProducer
from kafka.errors import KafkaError
from time import sleep

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# List of the interested topics
KEYWORDS_LIST = []
KEYWORDS_LIST += filter(
    bool, os.environ.get('KEYWORDS_LIST', '').split(','))

#Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

# Kafka Configurations
KAFKA_ENV_KAFKA_HOST_NAME = os.environ.get('KAFKA_HOST_NAME')
KAFKA_TOPIC_NAME = os.environ.get('KAFKA_TOPIC_NAME')

producer = KafkaProducer(bootstrap_servers=[KAFKA_ENV_KAFKA_HOST_NAME])

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (str(data))
        future = producer.send(KAFKA_TOPIC_NAME, str(data))
        record_metadata = future.get(timeout=10)
        print (record_metadata.topic)
        print (record_metadata.partition)
        print (record_metadata.offset)
        return True

    def on_error(self,status):
        print(status)

def main():
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)
    stream.filter(track=KEYWORDS_LIST)


if __name__ == "__main__":
    main()
