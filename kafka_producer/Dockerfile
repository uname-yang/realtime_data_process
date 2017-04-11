FROM python:2.7

# Install Pip
RUN apt-get update
RUN apt-get install -y python-pip

# Install and configure python packages
RUN pip install kafka-python
RUN pip install tweepy

# Copy python app
ADD ./twitter_kafka_producer.py /

# Start the Kafka producer process
CMD ["python","/twitter_kafka_producer.py"]
