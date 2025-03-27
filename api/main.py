from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import CONFIG
from .db.config import engine
from .db.tables import Base
from .v1.router import api_v1

app = FastAPI(title="Weather API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.api.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_v1, prefix="/v1", tags=["v1"])


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
