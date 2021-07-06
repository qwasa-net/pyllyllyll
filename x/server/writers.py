"""Server writers."""
import logging
import socket
import asyncio

from x.server.content import ContentGenerator


def writer(client: socket.socket, client_address: socket.AddressInfo, writer_id: int) -> tuple:
    """Handle a client -- write data, close connection."""

    logging.info("writer %s accepted connection from %s", writer_id, client_address)

    # get answer
    rsp = ContentGenerator.get()

    # send answer
    client.sendall(rsp)

    # close client (shutdown shared socket for all processes)
    client.shutdown(socket.SHUT_RDWR)
    client.close()

    logging.info("writer %s sent %.32s to %s, connection closed", writer_id, rsp, client_address)

    return (repr(rsp), writer_id)


async def writer_async(client: socket.socket, client_address: socket.AddressInfo, writer_id: int) -> tuple:
    """Handle a client -- write data, close connection. (ASYNC version)."""

    logging.info("writer %s accepted connection from %s", writer_id, client_address)
    loop = asyncio.get_event_loop()

    # get answer
    rsp = await ContentGenerator.get_async()

    # send answer
    await loop.sock_sendall(client, rsp)

    # close client (shutdown shared socket for all processes)
    client.shutdown(socket.SHUT_RDWR)
    client.close()

    logging.info("writer %s sent %.32s to %s, connection closed", writer_id, rsp, client_address)

    return (repr(rsp), writer_id)
