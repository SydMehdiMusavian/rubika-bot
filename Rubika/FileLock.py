import asyncio

class GlobalFileLock:
    _lock = asyncio.Lock()

    @classmethod
    def get_lock(cls):
        return cls._lock