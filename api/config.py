from json import load
from os import getcwd, getenv
from os.path import exists, join
from typing import List, Literal

from pydantic import BaseModel, ValidationError


class DatabaseConfig(BaseModel):
    engine: str = "sqlite"
    echo_sql: bool = False


class APIConfig(BaseModel):
    allowed_origins: List[str] = []


class NWSConfig(BaseModel):
    retry_attempts: int = 3
    user_agent_identifier: str
    user_agent_email: str
    test_lat: float
    test_long: float


class MapboxConfig(BaseModel):
    public_token: str


class Config(BaseModel):
    env: Literal["dev", "prod"]
    debug: bool = False
    api: APIConfig
    db: DatabaseConfig
    nws: NWSConfig
    mapbox: MapboxConfig


def create_config() -> Config:
    env = getenv("ENV", "dev")
    CONFIG_FILEPATH = join(getcwd(), config_filename := f"{env}.env.json")

    if not exists(CONFIG_FILEPATH):
        raise EnvironmentError(f"Config file {config_filename} not found")

    with open(CONFIG_FILEPATH) as file:
        raw_config = load(file)
        raw_config["env"] = env

    try:
        return Config(**raw_config)  # uses pydantic to validate shape and types
    except ValidationError as e:
        raise EnvironmentError(str(e.errors()))


CONFIG = create_config()
