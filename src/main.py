import multiprocessing as mp
from multiprocessing import Process
from server_v1.server_class import CustomerServe


def start_server_process():
    object = CustomerServe()
    object.initialize_slot()
    object.initialize_consumer()
    object.serve()


process_queue = []

for _ in range(4):
    process_queue.append(Process(start_server_process()))

for process in process_queue:
    process.start()
