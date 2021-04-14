from typing import Optional

from fastapi import APIRouter, HTTPException, Header, Request

from app import models, services

router = APIRouter()

tag_service = services.tag_instance
word_service = services.word_instance


@router.post("/words", tags=["word"])
def create_word(word_create: models.WordCreate, session_id: Optional[str] = Header(None)):
    """ 新規単語の追加
        意味を分解して知ってる単語、知らない単語に分ける
        知らない単語はDBに追加される
        知っている単語、知らない単語の中からランダムで一つ選んで返す
    """
    ret_data = word_service.create(word_create, session_id)
    if not ret_data:
        raise HTTPException(status_code=404, detail="word already.")
    return ret_data


@router.get("/words/{word}", response_model=models.WordAll, tags=["word"])
def get_word(word: str):
    """ 単語情報取得
    """
    ret_word = word_service.get(word)
    if not ret_word:
        raise HTTPException(status_code=200, detail="unknown word.")
    return ret_word


@router.put("/word_mean", response_model=models.WordAll, tags=["word"])
def update_word_mean(word_update: models.WordUpdate, session_id: Optional[str] = Header(None)):
    """ 単語情報更新
    """
    ret_word = word_service.update_mean(word_update.word, word_update.mean, session_id)
    if not ret_word:
        raise HTTPException(status_code=404, detail="unknown word.")
    return ret_word


@router.put("/word_good/{word}", response_model=models.WordAll, tags=["word"])
def update_word_good(word: str):
    """ good加算
    """
    ret_word = word_service.add_good(word)
    if not ret_word:
        raise HTTPException(status_code=404, detail="unknown word.")
    return {"detail": "success"}


@router.put("/word_bad/{word}", response_model=models.WordAll, tags=["word"])
def update_word_bad(word: str):
    """ bad加算
    """
    ret_word = word_service.add_bad(word)
    if not ret_word:
        raise HTTPException(status_code=404, detail="unknown word.")
    return {"detail": "success"}


@router.put("/word_kind", tags=["word"])
def update_word_kind(word_update: models.WordUpdateKind):
    """ 単語情報更新：タグ追加
    """
    if not word_service.update_kind(word_update.word, word_update.kind):
        raise HTTPException(status_code=404, detail="Word not found.")
    return {"detail": "success"}


@router.put("/word_tag_add", tags=["word"])
def add_word_tag(add_tag: models.WordAddTag):
    """ 単語情報更新：タグ追加
    """
    if not word_service.add_tag(add_tag.word, add_tag.tag):
        raise HTTPException(status_code=404, detail="Word not found.")
    return {"detail": "success"}


@router.put("/word_tag_add_text", tags=["word"])
def add_word_tag_text(add_tag: models.WordAddTagText):
    """ 単語情報更新：文章内からタグ追加
    """
    data = word_service.add_tag_for_text(add_tag.word, add_tag.text)
    if not data:
        raise HTTPException(status_code=200, detail="Tag not found.")
    return data


@router.get("/common_tag_word", tags=["word"])
def get_common_tag_word(word: str, tag: str):
    """ 共通タグの単語情報取得
    """
    data = word_service.get_common_tag_word(word, tag)
    if not data:
        raise HTTPException(status_code=200, detail="Not found.")
    return data


@router.delete("/unknown/{word}", tags=["word"])
def delete_unknown(word: str):
    """ 知らない単語削除
    """
    word_service.delete_unknown(word)
    return {"detail": "success"}


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
        raise HTTPException(status_code=200, detail="Not found.")
    return word


@router.get("/words_topic_unknown", tags=["word"])
def get_topic_unknown():
    """ 意味を知らない単語の中から一つピックアップして取得
    """
    unknown_data = word_service.get_topic_unknown()
    if not unknown_data:
        raise HTTPException(status_code=200, detail="Not found.")
    return unknown_data


@router.get("/words_topic_word", response_model=models.WordAll, tags=["word"])
def get_topic_word(session_id: Optional[str] = Header(None)):
    """ 自分が教えていない単語の中から一つピックアップして取得
    """
    word = word_service.get_topic_word(session_id)
    if not word:
        raise HTTPException(status_code=200, detail="Not found.")
    return word


@router.post("/remembered_tweet", tags=["word"])
def remembered_tweet():
    """ 直近で覚えたワードについてツイートする
    """
    word_service.remembered_tweet()
    return {"detail": "success"}


@router.post("/tag_add_tweet", tags=["word"])
def tag_add_tweet(add_tag: models.WordAddTag):
    """ タグ追加についてツイートする
    """
    if word_service.word_tag_add_tweet(add_tag.word, add_tag.tag):
        return {"detail": "success"}
    else:
        raise HTTPException(status_code=404, detail="Tag not found.")
