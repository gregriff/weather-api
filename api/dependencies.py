from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.config import AsyncLocalSession
from api.services.nws.config import AUTH_HEADERS, BASE_URL


async def get_nws():
    """Connection pool for NWS API requests"""
    client = AsyncClient(base_url=BASE_URL, headers=AUTH_HEADERS, trust_env=False)
    try:
        yield client
    finally:
        await client.aclose()


async def get_db():
    """
    Creates a database session for each request
    """
    session = AsyncLocalSession()
    try:
        yield session
    finally:
        await session.close()


NWS = Annotated[AsyncClient, Depends(get_nws)]
DB = Annotated[AsyncSession, Depends(get_db)]
