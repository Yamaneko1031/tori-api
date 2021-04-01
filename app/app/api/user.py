from fastapi import APIRouter, Body, HTTPException

from app import models, services

router = APIRouter()
user_service = services.UserService()


@router.post("/users", response_model=models.User, tags=["user"])
def create_user(user_create: models.UserCreate):
    return user_service.create(user_create)


@router.get("/users/{id}", response_model=models.User, tags=["user"])
def get_user(id: str):
    user = user_service.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.put("/users/{id}", response_model=models.User, tags=["user"])
def update_user(id: str, user_update: models.UserUpdate):
    user = user_service.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user_service.update_user(id, user_update)


@router.delete("/users/{id}", response_model=models.User, tags=["user"])
def delete_user(id: str):
    user = user_service.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user_service.delete(id)