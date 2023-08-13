import logging
import multiprocessing as mp
from multiprocessing import Process
from server_v1.server_class import CustomerServe

logging.basicConfig(filename='serving.log', level=logging.DEBUG, format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('customer_serve_logger')

process_queue = []

for _ in range(4):
    process_queue.append(Process(CustomerServe().serve()))

logger.info(process_queue)

for process in range(len(process_queue)):
    process_queue[process].start()
