from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.message import router as message_router
from app.api.v1.endpoints.url import router as url_router
from app.api.v1.endpoints.screenshot import router as screenshot_router


router = APIRouter()

router.include_router(
    health_router,
)

router.include_router(
    message_router,
)

router.include_router(
    url_router,
)

router.include_router(
    screenshot_router,
)
