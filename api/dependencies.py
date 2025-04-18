from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.config import AsyncLocalSession
from api.services.mapbox.config import MAPBOX_BASE_URL
from api.services.nws.config import NWS_AUTH_HEADERS, NWS_BASE_URL


async def get_nws():
    """Connection pool for NWS API requests"""
    client = AsyncClient(
        base_url=NWS_BASE_URL, headers=NWS_AUTH_HEADERS, trust_env=False, timeout=10.0
    )
    try:
        yield client
    finally:
        await client.aclose()


async def get_mapbox():
    """Connection pool for Mapbox API requests"""
    client = AsyncClient(base_url=MAPBOX_BASE_URL, trust_env=False, timeout=5.0)
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
Mapbox = Annotated[AsyncClient, Depends(get_mapbox)]
DB = Annotated[AsyncSession, Depends(get_db)]
