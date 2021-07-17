"""
Async client impementation.

Unlimited concurrent connections.
"""

import asyncio
import logging
import socket

workers_running = 0
workers_running_max = 0


def run(connect: tuple, readers, limit) -> None:
    """Run asyncio."""
    asyncio.run(run_async(connect, readers, limit))


async def run_async(connect, readers, limit):
    """Run asynchronous client. Unlimited concurrent connections."""

    counter = 0

    loop = asyncio.get_event_loop()
    tasks = []

    # create tasks
    while counter < limit:
        counter += 1
        task = loop.create_task(reader_wrapper(connect, readers, counter), name=f"task#{counter}")
        tasks.append(task)

    # wait tasks
    for task in tasks:
        await task


async def reader_wrapper(connect, readers, reader_id):
    """Add some logging for worker."""
    global workers_running, workers_running_max

    workers_running += 1
    workers_running_max = max(workers_running_max, workers_running)
    logging.info("starting new worker %s / %s (%s running/%s max)", reader_id,
                 asyncio.current_task().get_name(), workers_running, workers_running_max)

    # Create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setblocking(False)

    loop = asyncio.get_event_loop()

    await loop.sock_connect(client, connect)
    await readers.reader_async(client, reader_id)

    workers_running -= 1
    logging.info("worker %s / %s is done (%s running/%s max)", reader_id,
                 asyncio.current_task().get_name(), workers_running, workers_running_max)


def stop():
    pass


def init():
    pass
