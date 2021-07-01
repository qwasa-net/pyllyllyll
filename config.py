"""PYLLYLLYLL default values."""

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 44987

CONTENT_DELAY = 0.1
CONTENT_MAX_VALUE = 10_000_000

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(process)d:%(threadName)s:%(filename)s.%(funcName)s — %(message)s"

LISTEN_BACKLOG = 25
POOL_MAX_SIZE = 8

CLIENT_LIMIT = 100
