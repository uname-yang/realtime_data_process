FROM python:2.7

# Install Pip
RUN apt-get update
RUN apt-get install -y python-pip

# Install and configure python packages
RUN pip install kafka-python
RUN pip install redis

# Copy python app
ADD ./kafka_processor.py /

# Start the Kafka producer process
CMD ["/usr/bin/python","/kafka_processor.py"]
