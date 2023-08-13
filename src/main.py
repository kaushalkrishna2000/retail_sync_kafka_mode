import logging
import multiprocessing as mp
from multiprocessing import Process
from server_v1.server_class import CustomerServe

logging.basicConfig(filename='serving.log', level=logging.DEBUG, format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('customer_serve_logger')

logger.info("Starting to capture log")


def start_serve():
    logger.info("Activating serving ...")
    CustomerServe().serve()


process_queue = []

for _ in range(4):
    proc = Process(start_serve())
    process_queue.append(proc)
    logger.info(f"Starting process {_ + 1}...")
    proc.start()

logger.info(process_queue)
