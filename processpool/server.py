"""Multiprocess server."""
import concurrent.futures
import logging
import socket

from config import LISTEN_BACKLOG, POOL_MAX_SIZE

pool = None


def run(listen: tuple, writers) -> None:
    """Run a multiprocess (via ProcessPool) server."""

    # create a server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.bind(listen)
    server.listen(LISTEN_BACKLOG)
    counter = 0

    while True:

        # accept connections from outside (blocking call)
        (client, client_address) = server.accept()
        counter += 1

        # push (submit) new client to the pool
        future = pool.submit(writers.writer, client, client_address, counter)
        logging.info("created future #%s %s", counter, future)
        future.add_done_callback(future_callback)


def init():
    global pool
    pool = concurrent.futures.ProcessPoolExecutor(POOL_MAX_SIZE)


def stop():
    pool.shutdown()


def future_callback(future):
    logging.info("future running=%s, done=%s, exception=%s, result=%s", future.running(), future.done(),
                 future.exception(), future.result())
