from __future__ import annotations
import time
from typing import Any, Dict, Optional, Tuple
import aiohttp

class HTTPClient:
    """
    Shared aiohttp session (reduces latency vs creating a session per request).
    Includes a tiny in-memory TTL cache for GET requests.
    """

    def __init__(self, timeout_seconds: int = 8) -> None:
        self.timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        self.session: Optional[aiohttp.ClientSession] = None
        self._cache: Dict[str, Tuple[float, Any]] = {}  # url -> (expires_at, data)

    async def start(self) -> None:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self.timeout)

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    def _get_cached(self, url: str) -> Optional[Any]:
        item = self._cache.get(url)
        if not item:
            return None
        expires_at, data = item
        if time.time() > expires_at:
            self._cache.pop(url, None)
            return None
        return data

    async def get_json(self, url: str, ttl_seconds: int = 30) -> Any:
        cached = self._get_cached(url)
        if cached is not None:
            return cached

        if not self.session:
            raise RuntimeError("HTTPClient not started. Call await start().")

        async with self.session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.json()

        self._cache[url] = (time.time() + ttl_seconds, data)
        return data