"""Content generator (just random numbers)."""
import asyncio
import random
import time

from config import CONTENT_DELAY, CONTENT_MAX_VALUE


class ContentProcessor:
    """Content processor."""

    max_value = CONTENT_MAX_VALUE
    delay = CONTENT_DELAY
    delay_random = False
    sum = 0
    values = []

    @classmethod
    def configure(cls, args):
        """Set generator parameters."""
        if "content_delay" in args.__dict__:
            cls.delay = float(args.content_delay)
        if "content_delay_random" in args.__dict__:
            cls.delay_random = bool(args.content_delay_random)

    @classmethod
    def put(cls, data: bytes) -> int:
        """Process data."""
        time.sleep(cls.delay * (1.0 if not cls.delay_random else random.random()))
        answer = int(data.decode("utf8"))
        cls.values.append(answer)
        cls.sum += answer
        return cls.sum

    @classmethod
    async def put_async(cls, data: bytes) -> int:
        """Process data (ASYNC version)."""
        await asyncio.sleep(cls.delay * (1.0 if not cls.delay_random else random.random()))
        answer = int(data.decode("utf8"))
        cls.values.append(answer)
        cls.sum += answer
        return cls.sum

    @classmethod
    def result(cls) -> int:
        """Return result."""
        return cls.sum, len(cls.values)
