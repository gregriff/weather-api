from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.config import AsyncLocalSession


async def get_db():
    """
    Creates a database session for each request
    """
    session = AsyncLocalSession()
    try:
        yield session
    finally:
        await session.close()


DB = Annotated[AsyncSession, Depends(get_db)]
