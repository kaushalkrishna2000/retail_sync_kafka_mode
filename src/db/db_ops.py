import datetime
import logging
import os
from random import randint
import time

from models.customer import CustomerModel
from pymongo import ReturnDocument, MongoClient, UpdateOne

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('customer_serve_logger')

client = MongoClient(os.getenv("SRV") % (os.getenv("USERNAME"), os.getenv("PASSWORD")))

db = client['retail']
slot_collection = db['retail_slot']
item_collection = db['inventory']
price_collection = db['prices']


def db_select_assign_slot():
    logger.info(" Inside db assign function ")

    return slot_collection.find_one_and_update(
        filter={"assigned": "false"},
        update={"$set": {'assigned': 'true',
                         'empty': 'true',
                         'timestamp': str(datetime.datetime.utcnow())}},
        return_document=ReturnDocument.AFTER
    )


def db_select_clear_slot(id_proc):
    logger.info(" Inside db clear functions ")

    return slot_collection.find_one_and_update(
        filter={"_id": id_proc},
        update={"$set": {'assigned': 'false', 'timestamp': 'none',
                         'empty': 'true', 'count': 0}},
        return_document=ReturnDocument.BEFORE
    )


def db_status_ping():
    return client.admin.command('ping')


def db_mongo_proc(id_proc):
    return slot_collection.find_one({"_id": id_proc})


def process_customer_data(customer_data: CustomerModel, id_proc):
    logger.info("Inside process_customer_data")

    logger.info(f'{customer_data} at {os.getpid()} at {id_proc}')

    slot_collection.find_one_and_update(
        filter={"_id": id_proc},
        update={"$set": {'empty': 'false'}}
    )

    tot_cost = 0
    tot_time = 0
    bulk_operations = []

    for item, val in customer_data.item_list.items():
        price_tag = price_collection.find_one({'_id': item})
        item_time = price_tag['time']
        item_price = price_tag['price']

        bulk_operations.append(
            UpdateOne(
                {'_id': item},
                {
                    '$inc':
                        {
                            'qty': val,
                            'cost': val * item_price,
                            'time': val * item_time
                        }
                },
                upsert=True
            )
        )

        tot_cost += val * item_price
        tot_time += val * item_time

    item_collection.bulk_write(bulk_operations)

    sleep_time = tot_time + id_proc // 2000
    logger.info(f"Sleeping for {sleep_time}")
    time.sleep(sleep_time)
    logger.info(f"Sleeping done ....")

    slot_collection.find_one_and_update(
        filter={"_id": id_proc},
        update={"$inc": {"count": 1}, "$set": {'empty': 'true'}}
    )

    return "SUCCESSFUL EXECUTION SYNC"
