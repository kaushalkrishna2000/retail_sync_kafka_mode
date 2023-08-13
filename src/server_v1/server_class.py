import json
import os
import time

from models.customer import CustomerModel
from db import db_ops
from confluent_kafka import Consumer
import logging

logging.basicConfig(filename='serving.log',level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('customer_serve_logger')


class CustomerServe:

    def __init__(self):
        self.id_proc = None
        self.consumer = None

    def initialize_slot(self):
        doc = db_ops.db_select_assign_slot()

        self.id_proc = doc['_id']
        logger.info(f"{doc} and {self.id_proc} allotted to process {os.getpid()}")

    def initialize_consumer(self):
        props = {
            "bootstrap.servers": os.getenv("KAFKA_SERVER"),
            "sasl.mechanisms": "PLAIN",
            "security.protocol": "SASL_SSL",
            "sasl.username": os.getenv("KAFKA_USERNAME"),
            "sasl.password": os.getenv("KAFKA_PASSWORD"),
            "session.timeout.ms": 45000,
            "group.id": "retail-sync-python-group-1",
            "auto.offset.reset": "earliest",
            "client.id": f"client_{self.id_proc}"
        }

        self.consumer = Consumer(props)
        self.consumer.subscribe([f'topic_line_{self.id_proc}'])

        logger.info(f"Subscribed to topic_line_{self.id_proc} !!! ")

    def serve(self):

        self.initialize_slot()
        self.initialize_consumer()

        logger.info("Sleeping for 120 seconds to fully setup....")
        time.sleep(120)
        logger.info("Inside customer serve endpoint ......")

        try:
            while True:

                msg = self.consumer.poll(1.0)
                logger.info(f"Message from topic = {msg}")

                if msg is not None and msg.error() is None:
                    logger.info(
                        "value = {value:12}".format(key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

                    customer_dict = dict(msg)
                    customer_data = CustomerModel(**customer_dict)
                    logger.info(f"Customer data = {customer_data}")

                    db_ops.process_customer_data(customer_data, self.id_proc)

        except:

            logger.error(f"An error in getting message {msg.error()}")
            self.consumer.close()
