from fastapi import APIRouter

from src.presentation.api.v1.users import router as users_router

router = APIRouter(prefix="/v1", tags=["Users API"])
router.include_router(users_router)
