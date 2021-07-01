"""Async server impementation."""
import asyncio
import socket

from config import LISTEN_BACKLOG


async def run_async(listen, writers):
    """Run asynchronous server. Unlimited concurrent clients."""

    # create a server socket — NOT BLOCKING
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(listen)
    server.listen(LISTEN_BACKLOG)
    server.setblocking(False)
    counter = 0

    loop = asyncio.get_event_loop()
    while True:

        # accept connections from outside
        client, client_address = await loop.sock_accept(server)
        counter += 1

        # serve new client
        loop.create_task(writers.writer_async(client, client_address, counter))


def run(listen: tuple, writers) -> None:
    """Run asyncio."""

    asyncio.run(run_async(listen, writers))


def stop():
    pass


def init():
    pass
