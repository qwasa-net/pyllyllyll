"""Simple iterative server impementation. Only one client is served at a time."""

import socket

from config import LISTEN_BACKLOG


def run(listen: tuple, writers) -> None:
    """Run an iterative server, never stop."""

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

        # serve the client
        writers.writer(client, client_address, counter)


def init():
    pass


def stop():
    pass
