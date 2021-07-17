"""
Multithread client.

Unlimited number of threads,
a new thread is created for every client connection.
"""

import socket
import logging
import threading

threads_running = 0
threads_running_max = 0
threads = []


def run(connect: tuple, readers, limit: int = 100) -> None:
    """Run a multithread client."""

    counter = 0

    while counter < limit:

        counter += 1

        # create a new thread and serve the client
        thread = threading.Thread(target=reader_wrapper,
                                  args=(connect, readers.reader, counter),
                                  name=f"thread#{counter}")
        thread.start()
        threads.append(thread)


def reader_wrapper(connect, reader, *args, **kwargs):
    """Add some logging for worker."""
    global threads_running, threads_running_max

    threads_running += 1
    threads_running_max = max(threads_running_max, threads_running)
    logging.info("starting new thread %s (%s running/%s max)",
                 threading.current_thread().getName(), threads_running, threads_running_max)

    # Create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(connect)

    # call worker
    reader(client, *args, **kwargs)

    threads_running -= 1
    logging.info("thread %s is done (%s running/%s max)",
                 threading.current_thread().getName(), threads_running, threads_running_max)


def init():
    pass


def stop():
    """Wait for all threads we created."""
    for thread in threads:
        thread.join()
        logging.info("thread %s finished", thread.getName())
    logging.info("max number of running threads = %s", threads_running_max)
