from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.business.models.user import CreateUserRequest, UpdateUserRequest, User
from src.shared.di import singletons
from src.shared.logger import logger

router = APIRouter()


@router.get("/users", response_model=list[User])
def get_users() -> list[User]:
    user_service = singletons.user_service
    users = user_service.get_all()
    logger.info("users_listed", count=len(users))
    return users


@router.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int) -> Any:
    user_service = singletons.user_service
    user = user_service.get_by_id(user_id)
    if user is None:
        return JSONResponse(status_code=404, content={"detail": "User not found"})
    logger.info("user_fetched", user_id=user_id, user=user.model_dump())
    return user


@router.post("/users", response_model=User, status_code=201)
def create_user(body: CreateUserRequest) -> Any:
    user_service = singletons.user_service
    try:
        result = user_service.create_user(name=body.name, email=body.email, age=body.age)
        logger.info("user_created", user_id=result.id, user=result.model_dump())
        return result
    except ValidationError as e:
        logger.error("validation_error", context="create_user", error=str(e))
        return JSONResponse(status_code=400, content={"detail": "Validation error"})
    except Exception as e:
        logger.error("unexpected_error", context="create_user", error=str(e))
        return JSONResponse(status_code=500, content={"detail": "Unexpected error"})


@router.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, body: UpdateUserRequest) -> Any:
    user_service = singletons.user_service
    try:
        user = user_service.get_by_id(user_id)
        if user is None:
            return JSONResponse(status_code=404, content={"detail": "User not found"})
        updated = user_service.update_user(
            user_id=user_id,
            name=body.name,
            email=body.email,
            age=body.age,
        )
        logger.info("user_updated", user_id=user_id, user=updated.model_dump() if updated else None)
        return updated
    except ValidationError as e:
        logger.error("validation_error", context="update_user", user_id=user_id, error=str(e))
        return JSONResponse(status_code=400, content={"detail": "Validation error"})
    except Exception as e:
        logger.error("unexpected_error", context="update_user", user_id=user_id, error=str(e))
        return JSONResponse(status_code=500, content={"detail": "Unexpected error"})
