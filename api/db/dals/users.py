from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import defer

from api.db.tables import User


async def get_user(db: AsyncSession, user_id: int, with_settings: bool = True):
    if with_settings:
        return await db.get(User, user_id)
    return await db.get(User, user_id, options=[defer(User.settings)])
