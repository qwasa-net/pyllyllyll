"""Server starter."""
import argparse
import logging

import config

import server.writers as writers
from server.content import ContentGenerator


def main():
    """Set up and start server."""

    args = read_args()
    configure_logger(args)
    ContentGenerator.configure(args)

    # start server
    logging.info("starting %s server at %s:%s, kill me with [CTRL]+[C]", args.type, args.host, args.port)

    try:
        server = get_server(args.type)
        server.init()
        server.run(listen=(args.host, args.port), writers=writers)
    except KeyboardInterrupt:
        logging.info("got KeyboardInterrupt — stopping …")
        server.stop()
    except Exception as x:
        logging.error("server exited with an error: %s", x)

    logging.info("done")


def read_args():
    """Read cli arguments."""

    parser = argparse.ArgumentParser(description="PYLLYLLYLL")
    parser.add_argument("--type", type=str, default="solo")
    parser.add_argument("--host", type=str, default=config.LISTEN_HOST)
    parser.add_argument("--port", type=int, default=config.LISTEN_PORT)
    parser.add_argument("--content-delay", type=float, default=config.CONTENT_DELAY)
    parser.add_argument("--content-delay-random", action="store_true")
    parser.add_argument("--log-level", type=str, default=logging.INFO)
    return parser.parse_args()


def configure_logger(args):
    """Configure default logger."""

    logger = logging.getLogger()
    logger.setLevel(args.log_level if "log_level" in args.__dict__ else logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(config.LOG_FORMAT))
    logger.addHandler(handler)


def get_server(server_type: str = "solo"):
    """Get server module by type."""

    if server_type == "solo":
        import solo.server as server_module
    elif server_type == "multithread":
        import multithread.server as server_module
    elif server_type == "multiprocess":
        import multiprocess.server as server_module
    elif server_type == "threadpool":
        import threadpool.server as server_module
    elif server_type == "processpool":
        import processpool.server as server_module
    elif server_type == "asynchronous":
        import asynchronous.server as server_module
    else:
        raise Exception(f"unknown server type `{server_type}`")
    return server_module


if __name__ == "__main__":
    main()
