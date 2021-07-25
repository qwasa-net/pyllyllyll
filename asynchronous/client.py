"""
Async client implementation.

Semaphore-limited concurrent connections.
"""

import asyncio
import logging
import socket

from config import POOL_MAX_SIZE

# counters for simultaneously running workers
workers_running = 0
workers_running_max = 0

# semaphore to limit number of workers
pool_tickets = None


def run(connect: tuple, readers, limit) -> None:
    """Run client, run."""
    asyncio.run(run_async(connect, readers, limit))


async def run_async(connect, readers, limit):
    """Run asynchronous client. Unlimited concurrent connections."""
    global pool_tickets

    # init semaphore
    pool_tickets = asyncio.Semaphore(POOL_MAX_SIZE)
    loop = asyncio.get_event_loop()

    counter = 0
    tasks = []

    # create tasks
    while counter < limit:

        # block here and wait for the slot in the pool
        await pool_tickets.acquire()

        counter += 1
        task = loop.create_task(reader_wrapper(connect, readers, counter), name=f"task#{counter}")

        tasks.append(task)

    # wait tasks
    for task in tasks:
        await task


async def reader_wrapper(connect, readers, reader_id):
    """Add some stats and logging for the worker."""
    global workers_running, workers_running_max, pool_tickets

    workers_running += 1
    workers_running_max = max(workers_running_max, workers_running)
    logging.info("starting new worker %s / %s (%s running/%s max)", reader_id,
                 asyncio.current_task().get_name(), workers_running, workers_running_max)

    # Create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setblocking(False)

    # connect to the server
    loop = asyncio.get_event_loop()
    await loop.sock_connect(client, connect)

    # call the reader
    await readers.reader_async(client, reader_id)

    workers_running -= 1
    logging.info("worker %s / %s is done (%s running/%s max)", reader_id,
                 asyncio.current_task().get_name(), workers_running, workers_running_max)

    # leave the pool here
    pool_tickets.release()


def stop():
    pass


def init():
    pass
