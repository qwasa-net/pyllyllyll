"""Simple iterative client implementation. Only one request at a time."""

import socket


def run(connect: tuple, readers, limit: int = 100) -> None:
    """Run an iterative client, never stop."""

    counter = 0

    while counter < limit:

        # Create a client socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(connect)
        counter += 1

        # process connection
        readers.reader(client, reader_id=counter)


def init():
    pass


def stop():
    pass
