from fastapi import APIRouter, Body, HTTPException

from app import models, services

router = APIRouter()

tag_service = services.tag_instance


@router.get("/tags", tags=["tag"])
def get_tags():
    data = [
        tag_service.get_tags(0),
        tag_service.get_tags(1)
    ]
    return data


# @router.put("/tag1/{word}", tags=["tag"])
# def use_tag1(word: str):
#     if not tag_service.use_tag(word, 0):
#         return {"detail":"miss"}
#     return {"detail":"success"}


# @router.put("/tag2/{word}", tags=["tag"])
# def use_tag1(word: str):
#     tag_service.use_tag(word, 1)
#     return {"detail":"success"}
