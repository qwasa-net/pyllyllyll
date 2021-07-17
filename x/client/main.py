"""Server starter."""
import argparse
import logging
import time

import config
import x.client.readers as readers
from x.client.content import ContentProcessor


def main():
    """Set up and start server."""

    args = read_args()
    configure_logger(args)
    ContentProcessor.configure(args)

    # start server
    logging.info("starting %s server at %s:%s, kill me with [CTRL]+[C]", args.type, args.host, args.port)
    try:
        client = get_client(args.type)
        client.init()
        client.run(connect=(args.host, args.port), readers=readers, limit=args.limit)
    except KeyboardInterrupt:
        logging.info("got KeyboardInterrupt — stopping…")
    except Exception as x:
        logging.error("server exited with an error: %s", x)

    client.stop()
    time.sleep(0.25)
    logging.info("result = %s", ContentProcessor.result())
    logging.info("done")


def read_args():
    """Read cli arguments."""
    parser = argparse.ArgumentParser(description="PYLLYLLYLL")
    parser.add_argument("--host", type=str, default=config.LISTEN_HOST)
    parser.add_argument("--port", type=int, default=config.LISTEN_PORT)
    parser.add_argument("--limit", type=int, default=config.CLIENT_LIMIT)
    parser.add_argument("--content-delay", type=float, default=config.CONTENT_DELAY)
    parser.add_argument("--content-delay-random", action="store_true")
    parser.add_argument("--log-level", type=str, default=logging.INFO)
    parser.add_argument("--type", type=str, default="solo")
    return parser.parse_args()


def configure_logger(args):
    """Configure default logger."""
    logger = logging.getLogger()
    logger.setLevel(args.log_level if "log_level" in args.__dict__ else logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(config.LOG_FORMAT))
    logger.addHandler(handler)


def get_client(client_type: str = "solo"):
    """Get server module by type."""
    if client_type == "solo":
        import solo.client as client_module
    elif client_type == "multithread":
        import multithread.client as client_module
    elif client_type == "threadpool":
        import threadpool.client as client_module
    elif client_type == "asynchronous":
        import asynchronous.client as client_module
    else:
        raise Exception(f"unknown client type `{client_type}`")
    return client_module


if __name__ == "__main__":
    main()
