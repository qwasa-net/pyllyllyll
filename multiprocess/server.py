"""
Multi-process server.

Unlimited number of sub-processes,
a new process is forked for every new client connection.
"""
import logging
import os
import socket
import sys

from config import LISTEN_BACKLOG


def run(listen: tuple, writers) -> None:
    """Run an multiprocess server."""

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

        # create a new proccess to handle a new client
        child_pid = os.fork()
        if child_pid:  # in the PARENT process
            client.close()
            logging.info("forked new child process #%s pid=%s", counter, child_pid)
        else:  # in the child process
            server.close()
            rc = writers.writer(client, client_address, counter)
            logging.info("child process #%s is done pid=%s (rc=%s)", counter, os.getpid(), rc)
            sys.exit(0)


def init():
    pass


def stop():
    pass
