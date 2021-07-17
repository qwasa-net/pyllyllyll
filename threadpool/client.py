"""Simple iterative client implementation. Only one request at a time."""

import concurrent.futures
import logging
import socket
import threading

from config import POOL_MAX_SIZE

pool = None

workers_running = 0
workers_running_max = 0


def run(connect: tuple, readers, limit: int = 100) -> None:
    """Run an iterative client, never stop."""

    counter = 0

    while counter < limit:

        counter += 1

        # push (submit) new client to the pool
        future = pool.submit(reader_wrapper, connect, readers.reader, counter)
        future.add_done_callback(future_callback)
        logging.info("created future %s", future)


def reader_wrapper(connect, reader, reader_id):
    """Add some logging for reader worker."""
    global workers_running_max, workers_running

    # Create a client socket, connect
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(connect)

    workers_running += 1
    workers_running_max = max(workers_running_max, workers_running)
    logging.info("worker %s started in thread %s (%s running/%s max)", reader_id,
                 threading.current_thread().getName(), workers_running, workers_running_max)

    # call worker
    reader(client, reader_id)

    workers_running -= 1
    logging.info("worker %s is done in thread %s (%s running/%s max)", reader_id,
                 threading.current_thread().getName(), workers_running, workers_running_max)


def future_callback(future):
    logging.info("future running=%s, done=%s, exception=%s, result=%s", future.running(), future.done(),
                 future.exception(), future.result())


def init():
    global pool
    pool = concurrent.futures.ThreadPoolExecutor(POOL_MAX_SIZE)


def stop():
    pool.shutdown()
