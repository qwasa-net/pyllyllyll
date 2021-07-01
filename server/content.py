"""Content generator (just random numbers)."""
import asyncio
import random
import time

from config import CONTENT_DELAY, CONTENT_MAX_VALUE


class ContentGenerator:
    """Content generator."""

    max_value = CONTENT_MAX_VALUE
    delay = CONTENT_DELAY
    delay_random = False

    @classmethod
    def configure(cls, args):
        """Set generator parameters."""
        if "content_delay" in args.__dict__:
            cls.delay = float(args.content_delay)
        if "content_delay_random" in args.__dict__:
            cls.delay_random = bool(args.content_delay_random)

    @classmethod
    def get(cls) -> bytes:
        """Get an answer."""
        time.sleep(cls.delay * (1.0 if not cls.delay_random else random.random()))
        return str(random.randint(0, cls.max_value)).encode("utf8")

    @classmethod
    async def get_async(cls) -> bytes:
        """Get an answer (ASYNC version)."""
        asyncio.sleep(cls.delay * (1.0 if not cls.delay_random else random.random()))
        return str(random.randint(0, cls.max_value)).encode("utf8")
