from typing import Optional

from fastapi import APIRouter, HTTPException, Header

from app import models, services

router = APIRouter()
word_service = services.WordService()


@router.post("/words", tags=["word"])
def create_word(word_create: models.WordCreate, session_id: Optional[str] = Header(None)):
    """ 新規単語の追加
        意味を分解して知ってる単語、知らない単語に分ける
        知らない単語はDBに追加される
        知っている単語、知らない単語の中からランダムで一つ選んで返す
    """
    create_data = word_service.create(word_create, session_id)
    retData = word_service.get_knowns_list(
        mean=word_create.mean, teach_word=word_create.word)
    retData["create"] = create_data
    return retData


@router.get("/words/{word}", response_model=models.WordAll, tags=["word"])
def get_word(word: str):
    """ 単語情報取得
    """
    ret_word = word_service.get(word)
    if not ret_word:
        raise HTTPException(status_code=200, detail="unknown word.")
    return ret_word


@router.put("/words/", response_model=models.WordAll, tags=["word"])
def update_word(word_update: models.WordUpdate):
    """ 単語情報更新
    """
    ret_word = word_service.update(word_update)
    if not ret_word:
        raise HTTPException(status_code=200, detail="unknown word.")
    return ret_word


@router.get("/word_session", tags=["word"])
def get_session(session_id: Optional[str] = Header(None)):
    """ セッションID取得
        ヘッダーのsession_idパラメータに値が入っていない場合は新規idを発行
    """
    return {"session_id": word_service.get_session(session_id)}


@router.get("/words_topic_taught", response_model=models.WordAll, tags=["word"])
def get_topic_taught(session_id: Optional[str] = Header(None)):
    """ 教えた単語の中から一つピックアップして取得
    """
    word = word_service.get_topic_taught(session_id)
    if not word:
        raise HTTPException(status_code=200, detail="unknown")
    return word


@router.get("/words_topic_unknown", tags=["word"])
def get_topic_unknown():
    """ 意味を知らない単語の中から一つピックアップして取得
    """
    unknown_data = word_service.get_topic_unknown()
    if not unknown_data:
        raise HTTPException(status_code=200, detail="unknown")
    return unknown_data


@router.get("/words_topic_word", response_model=models.WordAll, tags=["word"])
def get_topic_word(session_id: Optional[str] = Header(None)):
    """ 自分が教えていない単語の中から一つピックアップして取得
    """
    word = word_service.get_topic_word(session_id)
    if not word:
        raise HTTPException(status_code=200, detail="unknown")
    return word
