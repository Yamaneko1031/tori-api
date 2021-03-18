from fastapi import APIRouter, Body, HTTPException

from app import models, services

router = APIRouter()
word_service = services.WordService()


@router.post("/words", response_model=models.WordAll, tags=["word"])
def create_word(word_create: models.WordCreate):
    return word_service.create(word_create)


@router.get("/words/{word}", response_model=models.WordAll, tags=["word"])
def get_word(word: str):
    ret_word = word_service.get(word)
    if not ret_word:
        raise HTTPException(status_code=200, detail="unknown word.")
    return ret_word


@router.put("/words/", response_model=models.WordAll, tags=["word"])
def get_word(word_update: models.WordUpdate):
    ret_word = word_service.update(word_update)
    if not ret_word:
        raise HTTPException(status_code=200, detail="unknown word.")
    return ret_word



@router.get("/words/{word}", response_model=models.WordAll, tags=["word"])
def get_word(word: str):
    ret_word = word_service.get(word)
    if not ret_word:
        raise HTTPException(status_code=200, detail="unknown")
    return ret_word



@router.get("/words/random/", response_model=models.WordAll, tags=["word"])
def get_word(word: str):
    ret_word = word_service.get(word)
    if not ret_word:
        raise HTTPException(status_code=200, detail="unknown")
    return ret_word
