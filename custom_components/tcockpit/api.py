"""Small async client for the TCockpit Home Assistant API (/api/ha/v1)."""
from __future__ import annotations

import secrets
from typing import Any

import aiohttp


class TCockpitAuthError(Exception):
    """API key missing, invalid or revoked."""


class TCockpitError(Exception):
    """Any other API error."""


class TCockpitApi:
    def __init__(self, session: aiohttp.ClientSession, base_url: str, api_key: str) -> None:
        self._session = session
        self._base = base_url.rstrip("/")
        self._key = api_key

    async def _request(self, method: str, path: str, body: dict | None = None) -> Any:
        headers = {"Authorization": f"Bearer {self._key}", "Accept": "application/json"}
        try:
            async with self._session.request(
                method, self._base + path, json=body if method == "POST" else None,
                headers=headers, timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                data = await resp.json(content_type=None)
                if resp.status == 401:
                    raise TCockpitAuthError((data or {}).get("message", "unauthorized"))
                if resp.status >= 400:
                    raise TCockpitError((data or {}).get("message", f"HTTP {resp.status}"))
                return data
        except aiohttp.ClientError as err:
            raise TCockpitError(str(err)) from err

    async def info(self) -> dict:
        return await self._request("GET", "/api/ha/v1/info")

    async def vehicles(self) -> list[dict]:
        return await self._request("GET", "/api/ha/v1/vehicles")

    async def state(self, vin: str) -> dict:
        return await self._request("GET", f"/api/ha/v1/vehicles/{vin}/state")

    async def command(self, vin: str, name: str) -> dict:
        # The TCockpit server queues it like an app command (wake, retry, push confirmation).
        return await self._request("POST", f"/api/ha/v1/vehicles/{vin}/commands/{name}",
                                   {"idempotencyKey": secrets.token_urlsafe(18)})
