import logging
import multiprocessing as mp
from multiprocessing import Process
from server_v1.server_class import CustomerServe

logging.basicConfig(filename='serving.log', level=logging.DEBUG, format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('customer_serve_logger')




def start_serve():
    logger.info("Activating serving ...")
    CustomerServe().serve()


if __name__=="__main__":

    logger.info("Starting to capture log")

    num_proc=4

    process_queue = []

    for _ in range(num_proc):
        proc = Process(name=f"SERVING_PROCESS_{_}",target=start_serve)
        process_queue.append(proc)
        logger.info(f"Starting process {_ + 1}...")
        proc.start()

    logger.info(process_queue)
