import os

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    asyncpg_url: PostgresDsn = os.getenv("POSTGRES_URL")
    psycopg2_url: PostgresDsn = os.getenv("POSTGRES_URL_SYNC")
    redis_url: RedisDsn = os.getenv("REDIS_URL") + os.getenv("REDIS_DB")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")
    jwt_expire: int = os.getenv("JWT_EXPIRE")


settings = Settings()
