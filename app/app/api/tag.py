from fastapi import APIRouter, Body, HTTPException

from app import models, services

router = APIRouter()

tag_service = services.tag_instance


@router.get("/tag", tags=["tag"])
def get_tag(tag: str):
    ret_data = tag_service.get_tag(tag)
    if not ret_data:
        raise HTTPException(status_code=404, detail="unknown tag_choices.")
    return ret_data


@router.get("/tag/choices", tags=["tag"])
def get_tag():
    ret_data = tag_service.get_random_choices()
    if not ret_data:
        raise HTTPException(status_code=404, detail="unknown tag_choices.")
    return ret_data


@router.get("/tag/more0", tags=["tag"])
def get_tag():
    ret_data = tag_service.get_random_tag_more0()
    if not ret_data:
        raise HTTPException(status_code=404, detail="unknown tag_more0.")
    return ret_data
