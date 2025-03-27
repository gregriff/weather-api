from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import undefer

from api.db.tables import User


async def get_user(db: AsyncSession, user_id: int):
    return await db.get(User, user_id)


async def get_user_with_settings(db: AsyncSession, user_id: int):
    """populates users->settings relationship with a join"""
    return await db.get(User, user_id, options=[undefer(User.settings)])
