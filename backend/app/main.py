from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from app.api.job import router as nonsense_router
from app.api.term import router as term_router
from app.utils.logging import AppLogger
from app.api.user import router as user_router
from app.api.health import router as health_router
from app.redis import get_redis
from app.services.auth import AuthBearer

logger = AppLogger().get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the redis connection
    app.state.redis = await get_redis()
    try:
        yield
    finally:
        # close redis connection and release the resources
        app.state.redis.close()


app = FastAPI(title="TTF API", version="0.1", lifespan=lifespan)

app.include_router(term_router)
app.include_router(nonsense_router)
app.include_router(user_router)


# app.include_router(health_router, prefix="/v1/public/health", tags=["Health, Public"])
app.include_router(health_router, prefix="/v1/health", tags=["Health, Bearer"], dependencies=[Depends(AuthBearer())])
