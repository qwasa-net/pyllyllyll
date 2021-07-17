"""Server writers."""
import asyncio
import logging
import socket

from x.client.content import ContentProcessor


def reader(client: socket.socket, reader_id: int) -> tuple:
    """Handle a connection -- read all data, close connection, call processor."""

    logging.info("reader %s connected", reader_id)

    # read all data till the end
    data = b""
    while True:
        chunk = client.recv(1024)
        if not chunk:
            break
        data += chunk

    # close client (shutdown shared socket for all processes)
    client.shutdown(socket.SHUT_RDWR)
    client.close()

    logging.info("reader %s read %s bytes, connection closed", reader_id, len(data))

    # process data
    rsp = ContentProcessor.put(data)

    logging.info("reader %s data processed %s", reader_id, rsp)

    return (repr(rsp), reader_id)


async def reader_async(client: socket.socket, reader_id: int) -> tuple:
    """Handle a connection -- read all data, close connection, call processor. (ASYNC version)."""

    logging.info("reader %s connected", reader_id)
    loop = asyncio.get_event_loop()

    # read all data till the end
    data = b""
    while True:
        chunk = await loop.sock_recv(client, 1024)
        if not chunk:
            break
        data += chunk

    # close client (shutdown shared socket for all processes)
    client.shutdown(socket.SHUT_RDWR)
    client.close()

    logging.info("reader %s read %s bytes, connection closed", reader_id, len(data))

    # process data
    rsp = await ContentProcessor.put_async(data)

    logging.info("reader %s data processed %s", reader_id, rsp)

    return (repr(rsp), reader_id)
