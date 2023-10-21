import asyncio

import async_timeout
from aiohttp import ClientSession
from core.config import Config
from exceptions import NetworkException


async def make_request(
    session: ClientSession,
    url: str,
    method: str,
    data: dict = {},
    params: dict = {},
    headers: dict = {},
):
    try:
        with async_timeout.timeout(Config.REQUEST_TIMEOUT):
            request = getattr(session, method)
            async with request(
                url, json=data, params=params, headers=headers
            ) as response:
                data = await response.json()
                if response.status > 399:
                    raise NetworkException(status_code=response.status, detail=data)
                return data
    except asyncio.TimeoutError:
        raise NetworkException(status_code=408, detail="Request timeout.")
