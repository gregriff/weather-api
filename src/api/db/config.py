from os.path import join
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ...api.config import CONFIG


def get_db_url():
    if CONFIG.db.engine != "sqlite":
        raise EnvironmentError("Only SQLite supported at this time")
    db_folder = Path(__file__).resolve().parent
    db_filepath = join(db_folder, "db.sqlite")
    return f"sqlite+aiosqlite:///{db_filepath}"


SQLALCHEMY_DATABASE_URL = get_db_url()

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=CONFIG.db.echo_sql,
    connect_args=dict(check_same_thread=False),
    pool_pre_ping=True,
)
AsyncLocalSession: async_sessionmaker[AsyncSession] = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)
