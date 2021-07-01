"""
Multithread server.

Unlimited number of threads,
a new thread is created for every client connection.
"""
import logging
import socket
import threading

from config import LISTEN_BACKLOG

threads_running = 0
threads_running_max = 0
threads = []


def run(listen: tuple, writers) -> None:
    """Run a multithread server."""

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

        # create a new thread and serve the client
        thread = threading.Thread(target=writer_wrapper,
                                  args=(writers.writer, client, client_address, counter),
                                  name=f"thread#{counter}")

        thread.start()

        # save for later
        threads.append(thread)


def stop():
    """Wait for all threads we created."""
    for thread in threads:
        thread.join()
        logging.info("thread %s finished", thread.getName())
    logging.info("max number of running threads = %s", threads_running_max)


def init():
    pass


def writer_wrapper(writer, *args, **kwargs):
    """Add some logging for worker."""
    global threads_running, threads_running_max

    threads_running += 1
    threads_running_max = max(threads_running_max, threads_running)

    logging.info("staring new thread %s (%s running)", threading.current_thread().getName(), threads_running)

    writer(*args, **kwargs)
    threads_running -= 1
