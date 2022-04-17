from typing import Optional
from app.models.user_log import TeachLogCreate

from fastapi import APIRouter, HTTPException, Header, Request

from app import models, services

router = APIRouter()

tag_service = services.tag_instance
word_service = services.word_instance
user_log_service = services.user_log_instance


@router.post("/words", tags=["word"])
def create_word(request: Request, word_create: models.WordCreate, session_id: Optional[str] = Header(None)):
    """ 新規単語の追加
        意味を分解して知ってる単語、知らない単語に分ける
        知らない単語はDBに追加される
        知っている単語、知らない単語の中からランダムで一つ選んで返す
    """
    ret_data = word_service.create(
        word_create, session_id, request.client.host)

    if not ret_data:
        raise HTTPException(status_code=404, detail="word already.")

    user_log_service.add_teach_log(
        word_create.word, word_create.mean, request.client.host, session_id, ret_data)

    return ret_data


@router.get("/words/{word}", response_model=models.WordAll, tags=["word"])
def get_word(word: str):
    """ 単語情報取得
    """
    ret_word = word_service.get(word)
    if not ret_word:
        raise HTTPException(status_code=200, detail="unknown word.")
    return ret_word


@router.delete("/words/{word}", tags=["word"])
def delete_word(word: str):
    """ 単語削除
    """
    word_service.delete(word)
    return {"detail": "success"}


@router.put("/word_mean", response_model=bool, tags=["word"])
def update_word_mean(request: Request, word_update: models.WordUpdate, session_id: Optional[str] = Header(None)):
    """ 単語情報更新
    """
    ret_word = word_service.update_mean(
        word_update.word, word_update.mean, session_id)
    if not ret_word:
        raise HTTPException(status_code=404, detail="unknown word.")
    return ret_word


@router.put("/word_good/{word}", tags=["word"])
def update_word_good(word: str):
    """ good加算
    """
    ret_word = word_service.add_good(word)
    if not ret_word:
        raise HTTPException(status_code=404, detail="unknown word.")
    return {"detail": "success"}


@router.put("/word_bad/{word}", tags=["word"])
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


@router.post("/delete_tweet/{id}", tags=["word"])
def delete_tweet(id: int):
    """ ツイートを削除する
    """
    if word_service.delete_tweet(id):
        return {"detail": "success"}
    else:
        return {"detail": "failed"}


@router.post("/remembered_tweet", tags=["word"])
def remembered_tweet():
    """ 直近で覚えたワードについてツイートする
    """
    word_service.remembered_tweet()
    return {"detail": "success"}


@router.post("/unknown_tweet", tags=["word"])
def unknown_tweet():
    """ 知らない単語についてツイートする
    """
    word_service.unknown_word_tweet()
    return {"detail": "success"}


@router.post("/known_tweet", tags=["word"])
def known_tweet():
    """ 知っている単語についてツイートする
    """
    word_service.known_word_tweet()
    return {"detail": "success"}


@router.post("/trend_tweet", tags=["word"])
def trend_tweet():
    """ ツイッタートレンドからランダムでピックアップしてツイートする
    """
    word_service.trend_tweet()
    return {"detail": "success"}


@router.post("/trend_tweet_force", tags=["word"])
def trend_tweet_force(word: str):
    """ 指定したトレンドワードをツイートする
    """
    word_service.trend_tweet_force(word)
    return {"detail": "success"}


@router.post("/relation_tag_tweet", tags=["word"])
def relation_tag_tweet():
    """ タグに関連する単語のツイート
    """
    word_service.word_relation_tag_tweet()
    return {"detail": "success"}


@router.post("/tag_add_tweet", tags=["word"])
def tag_add_tweet(add_tag: models.WordAddTag):
    """ タグ追加についてツイートする
    """
    if word_service.word_tag_add_tweet(add_tag.word, add_tag.tag):
        return {"detail": "success"}
    else:
        raise HTTPException(status_code=404, detail="Tag not found.")


@router.get("/word_temp/{id}", tags=["word"])
def get_temp(id: str):
    """ テンポラリから情報を取得する
    """
    ret = word_service.get_temp(id)
    if not ret:
        raise HTTPException(status_code=404, detail="Temp not found.")
    return ret


@router.get("/word_temp_front/{id}", tags=["word"])
def get_temp_front(id: str):
    """ テンポラリから情報を取得する
    """
    ret = word_service.get_temp_front(id)
    if not ret:
        raise HTTPException(status_code=404, detail="Temp not found.")
    return ret


@router.post("/janken_tweet", tags=["word"])
def janken_tweet():
    """ じゃんけんの結果をツイート
    """
    word_service.janken_tweet()
    return {"detail": "success"}


@router.post("/follow_back", tags=["word"])
def follow_back():
    """ フォローバック処理
    """
    word_service.follow_back()
    return {"detail": "success"}


@router.post("/create_temp_remember_word", tags=["word"])
def create_temp_remember_word(word: str):
    """ 覚えた単語の情報をテンポラリに保存
    """
    id = word_service.create_temp_remember_word(word)
    return {"id": id}


@router.post("/create_temp_fromt", tags=["word"])
def create_temp_fromt(word: str, cnt: int, session_id: Optional[str] = Header(None)):
    """ フロント側から情報をテンポラリに保存
    """
    set_id = "{}{}".format(session_id, cnt)
    id = word_service.create_temp_fromt(word, set_id)
    if not id:
        raise HTTPException(status_code=404, detail="Not found.")
    return {"detail": "success"}


@router.post("/test", tags=["word"])
def time_test(request: Request):
    """ テスト処理
    """
    # word_service.time_test()
    print(request.client.host)
    ret = word_service.post_tweet("テストしてるの！", request.client.host)
    user_log_service.add_teach_log(
        "word", "mean", request.client.host, "session_id", ret["stat"], ret["id"])
    return {"detail": "success"}
