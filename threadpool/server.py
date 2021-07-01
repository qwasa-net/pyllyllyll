"""Multithread (ThreadPoolExecutor) server."""
import logging
import socket
import threading
import concurrent.futures

from config import LISTEN_BACKLOG, POOL_MAX_SIZE

pool = None

workers_running = 0
workers_running_max = 0


def run(listen: tuple, writers) -> None:
    """Run a multithread (via ThreadPool) server."""

    # create a server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(listen)
    server.listen(LISTEN_BACKLOG)
    counter = 0

    while True:

        # accept connections from outside (blocking call)
        (client, client_address) = server.accept()
        counter += 1

        # push (submit) new client to the pool
        future = pool.submit(writer_wrapper, writers.writer, client, client_address, counter)
        future.add_done_callback(future_callback)
        logging.info("created future %s", future)


def writer_wrapper(writer, client, client_address, writer_id):
    """Add some logging for worker."""
    global workers_running_max, workers_running

    workers_running += 1
    workers_running_max = max(workers_running_max, workers_running)
    logging.info("worker %s started in thread %s (%s running/%s max)", writer_id,
                 threading.current_thread().getName(), workers_running, workers_running_max)

    # call worker
    writer(client, client_address, writer_id)

    workers_running -= 1
    logging.info("worker %s is done in thread %s (%s running/%s max)", writer_id,
                 threading.current_thread().getName(), workers_running, workers_running_max)


def init():
    global pool
    pool = concurrent.futures.ThreadPoolExecutor(POOL_MAX_SIZE)


def stop():
    pool.shutdown()


def future_callback(future):
    logging.info("future running=%s, done=%s, exception=%s, result=%s", future.running(), future.done(),
                 future.exception(), future.result())
