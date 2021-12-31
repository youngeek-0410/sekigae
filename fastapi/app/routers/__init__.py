from fastapi import APIRouter

from .monitoring import monitoring_router
from .v1 import api_v1_router

router = APIRouter()
router.include_router(monitoring_router, tags=["monitoring"])
router.include_router(api_v1_router, prefix="/api/v1", tags=["api/v1"])
