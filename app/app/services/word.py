import json
import os
import random
import logging
from uuid import uuid4
from datetime import datetime
from typing import List
import re
from xmlrpc.client import DateTime
import jaconv

import tweepy
from google.cloud.firestore_v1.transaction import Transaction
from google.cloud import firestore
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from pykakasi import kakasi

from app.util import morpheme
from app import models, services

kakasi = kakasi()
kakasi.setMode("J", "H")
hira_conv = kakasi.getConverter()

db = firestore.Client()
logger = logging.getLogger(__name__)

auth = tweepy.OAuthHandler(
    os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'],
                      os.environ['ACCESS_TOKEN_SECRET'])

tweet_api = tweepy.API(auth)

tag_service = services.tag_instance
system_service = services.system_instance


# date, datetimeの変換関数
def json_serial(obj):
    # 日付型の場合には、文字列に変換します
    if isinstance(obj, (datetime)):
        return obj.isoformat()
    if isinstance(obj, (DatetimeWithNanoseconds)):
        return ""
    
    # 上記以外はサポート対象外.
    raise TypeError ("Type %s not serializable" % type(obj))


@firestore.transactional
def create_tr(transaction: Transaction, word_create: models.WordCreate, tags: List[models.TagAct], taught: str,
              collect_word: str, collect_unknown: str, collect_session: str
              ):
    """ 新規単語の追加で呼び出すトランザクション処理
    """
    # unknownsコレクションにある場合は削除する
    docs = db.collection(collect_unknown).where(
        "word", "==", word_create.word).stream()
    for doc in docs:
        transaction.delete(doc._reference)
        system_service.dec_unknown()

    set_like = 0
    set_tags = []
    set_tags_cnt = {}
    for tag in tags:
        set_tags.append(tag["text"])
        set_tags_cnt[tag["text"]] = firestore.Increment(1)
        set_like = set_like + tag["pnt"]

    # wordsコレクションに追加
    word_data = models.WordAll(**word_create.dict()).dict()
    word_data["taught"] = taught
    word_data["like"] = set_like
    word_data["tags"] = set_tags
    word_data["tags_cnt"] = set_tags_cnt
    word_data["cnt"] = firestore.Increment(1)
    word_data["index"] = system_service.get_system_data()["word_cnt"]
    word_ref = db.collection(collect_word).document()
    transaction.set(word_ref, word_data)

    # sessionsコレクション更新
    session_ref = db.collection(
        collect_session).document(document_id=taught)
    session_data = {
        "teach_words": firestore.ArrayUnion([word_create.word]),
        "teach_refs": firestore.ArrayUnion([word_ref]),
        "teach_cnt": firestore.Increment(1),
    }
    transaction.set(session_ref, session_data, merge=True)

    return word_ref


class WordService:
    collection_system = "system"
    collection_name = "words"
    collection_unknown = "unknowns"
    collection_session = "sessions"
    collection_temporary = "temporaries"
    collection_tweet_log = "tweet_log"

    def __init__(self):
        """ コンストラクタ
        """
        # NGリスト取得
        self.renew_ng_list()

    def renew_ng_list(self):
        self.ng_list = system_service.get_ng_list()
        self.ng_regex = system_service.get_ng_regex()
        self.ng_ip = system_service.get_ng_ip()
        self.ng_session = system_service.get_ng_session()

    def create(self, word_create: models.WordCreate, taught: str, ip_address: str) -> models.WordAll:
        """ 新規単語の追加
        """
        self.renew_ng_list()
        
        retData = self.get_knowns_list(
            mean=word_create.mean, teach_word=word_create.word, secret_tag=word_create.secret_tag)

        docs = db.collection(self.collection_name).where(
            "word", "==", word_create.word).limit(1).get()

        if docs:
            if self.update_mean(word_create.word, word_create.mean, taught):
                retData["tweet"] = self.mean_update_tweet(
                    docs[0]._reference, taught, ip_address)
            ref = docs[0]._reference
            retData["action"] = "更新"
            retData["pre_mean"] = ref.get().to_dict()["word"]
        else:
            transaction = db.transaction()
            ref = create_tr(transaction=transaction,
                            word_create=word_create,
                            taught=taught,
                            tags=retData["tags"],
                            collect_word=self.collection_name,
                            collect_unknown=self.collection_unknown,
                            collect_session=self.collection_session
                            )
            system_service.add_word_create(word_create.word)
            retData["tweet"] = self.word_create_tweet(
                ref, word_create.secret_tag, taught, ip_address)
            retData["action"] = "新規"
            retData["pre_mean"] = ""

        retData["create"] = models.WordAll(**ref.get().to_dict())
        retData["create_ref"] = ref

        return retData

    def delete(self, word: str):
        """ 単語情報削除
        """
        docs = db.collection(self.collection_name).where(
            "word", "==", word).limit(1).get()
        for doc in docs:
            doc._reference.delete()
        return

    def delete_from_ref(self, word_ref):
        """ 単語情報削除
        """
        word_ref.delete()
        return

    def get(self, word: str) -> models.WordAll:
        """ 単語情報取得
        """
        docs = db.collection(self.collection_name).where(
            "word", "==", word).limit(1).get()
        if docs:
            return models.WordAll(**docs[0].to_dict())
        return

    def get_word_list_next(self, limit: int, next_key=None):
        """ 更新された
        google.api_core.datetime_helpers.DatetimeWithNanoseconds
        """

        doc_dict_list = []

        if next_key:
            # print(firestore.Timestamp.fromDate(DateTime(next_key)))
            
            docs = db.collection(self.collection_name).order_by(
                u'updated_at', direction=firestore.Query.DESCENDING).start_after({u'updated_at': next_key}).limit(limit).stream()

            for doc in docs:
                doc_dict_list.append(doc.to_dict())

        else:
            docs = db.collection(self.collection_name).order_by(
                u'updated_at', direction=firestore.Query.DESCENDING).limit(limit).stream()

            for doc in docs:
                doc_dict_list.append(doc.to_dict())
        
        next = doc_dict_list[-1]['updated_at']
        
        for word_data in doc_dict_list:
            for key, value in word_data.items():
                if isinstance(value, (DatetimeWithNanoseconds)):
                    print(value)
                    word_data[key] = ""

        # doc_dict_list = json.dumps(doc_dict_list, default=json_serial)
        # print(doc_dict_list)  
        # print(doc_dict_list[-1]['updated_at'])
        ret = {"doc": doc_dict_list, "next_key": next, "now_key": next_key}

        return ret

    # def get_word_list_prev(self, end_key=None):
    #     """ 更新された
    #     google.api_core.datetime_helpers.DatetimeWithNanoseconds
    #     """

    #     doc_dict_list = []

    #     if end_key:
    #         docs = db.collection(self.collection_name).order_by(
    #             u'updated_at', direction=firestore.Query.DESCENDING).end_before({u'updated_at': end_key}).limit_to_last(5).get()

    #         for doc in docs:
    #             doc_dict_list.append(doc.to_dict())

    #     else:
    #         docs = db.collection(self.collection_name).order_by(
    #             u'updated_at', direction=firestore.Query.DESCENDING).limit_to_last(5).stream()

    #         for doc in docs:
    #             doc_dict_list.append(doc.to_dict())

    #     for doc_dict in doc_dict_list:
    #         print(doc_dict["word"])

    #     return doc_dict_list[0]['updated_at']

    def get_common_tag_word(self, word: str, tag: str) -> models.WordAll:
        """ 共通タグの単語情報取得
        """
        data = []
        docs = db.collection("words").where(
            "tags", "array_contains", tag).stream()
        for doc in docs:
            if doc.to_dict()["word"] != word:
                data.append(doc)

        if data:
            return models.WordAll(**random.choice(data).to_dict())

        return

    def delete_unknown(self, word: str):
        """ 知らない単語情報削除
        """
        # unknownsコレクションにある場合は削除する
        docs = db.collection(self.collection_unknown).where(
            "word", "==", word).stream()
        for doc in docs:
            doc._reference.delete()
            system_service.dec_unknown()

        return

    def get_knowns_list(self, mean: str, teach_word: str = "", secret_tag: str = ""):
        """ 意味を分解して知ってる単語、知らない単語に分ける
            知らない単語はDBに追加される
            知っている単語、知らない単語の中からランダムで一つ選んで返す
        """
        # かな１文字判定用
        re_kana_1char = re.compile(r'[あ-ん]|[ア-ン]')
        # 意味の中から認識可能な単語を取得
        phrase_list = morpheme.disassemble(mean)
        phrase_list.update(morpheme.disassemble(secret_tag))

        word_ref = ""
        trend_word = ""

        # teach_wordに値が入っている場合は参照情報を保存する
        if teach_word:
            word_ref = teach_word
        # teach_wordに値が入って無い場合は入力ワードをトレンド情報に保存する
        else:
            trend_word = mean

        # 知っている単語、知らない単語の一覧を作成
        known_list = []
        unknown_list = []
        tag_list = []
        for key, value in phrase_list.items():
            tmp = tag_service.get_tag(key)
            if re_kana_1char.fullmatch(key):
                # かな1文字は除外
                pass
            elif tmp:
                # タグに存在する物は別枠
                tag_list.append(tmp)
            elif value == "形容動詞" or value == "形容詞":
                kana = hira_conv.do(key)
                tag_service.create_reserve_tags(key, value, 0, key, kana)
            else:
                docs = db.collection(self.collection_name).where(
                    "word", "==", key).limit(1).get()
                if docs:
                    known_list.append({"word": key, "kind": value})
                elif teach_word == key:
                    pass
                else:
                    unknown_list.append({"word": key, "kind": value})
                    unknown_ref = db.collection(
                        self.collection_unknown).document(key)
                    unknown_ref.set({
                        "word": key,
                        "kind": value,
                        "word_ref": word_ref,
                        "trend": trend_word,
                        "interest": firestore.Increment(1)
                    }, merge=True)
                    system_service.add_unknown(key)

        # 知っている単語、知らない単語の中からランダムで一つ選んで返す
        ret_data = {"known": 0, "unknown": 0, "tags": tag_list}
        if known_list:
            ret_data["known"] = random.choice(known_list)
        if unknown_list:
            ret_data["unknown"] = random.choice(unknown_list)

        return ret_data

    def get_topic_taught(self, taught: str, get_ref: bool = False) -> models.WordAll:
        """ 教えた単語の中から一つピックアップして取得
        """
        doc = db.collection(self.collection_session).document(
            document_id=taught).get()
        doc_dict = doc.to_dict()
        if "teach_refs" not in doc_dict:
            return
        ref = random.choice(doc.to_dict()["teach_refs"])
        if get_ref:
            return ref
        return models.WordAll(**ref.get().to_dict())

    def get_topic_unknown(self, limit: int = 20):
        """ 意味を知らない単語の中から一つピックアップして取得
        """
        get_data_list = []
        docs = db.collection(self.collection_unknown).order_by(
            u'interest', direction=firestore.Query.DESCENDING).limit(limit).stream()
        
        for doc in docs:
            unknown = doc.to_dict()
            if self.ng_text_check(unknown["word"]):
                continue
            ref = {
                "word": "",
                "mean": "",
            }
            if unknown["word_ref"]:
                get_word = self.get(unknown["word_ref"])
                if get_word:
                    ref["word"] = get_word.word
                    ref["mean"] = get_word.mean
                else:
                    print("word_refの先が存在しない:{}:{}".format(
                        doc.id, unknown["word_ref"]))

            get_data_list.append({
                "word": unknown["word"],
                "kind": unknown["kind"],
                "ref": {
                    "word": ref["word"],
                    "mean": ref["mean"],
                }
            })

        if not get_data_list:
            return

        return random.choice(get_data_list)

    def get_topic_word(self, taught: str = "", limit: int = 20, get_ref: bool = False) -> models.WordAll:
        """ 自分が教えていない単語の中から一つピックアップして取得
        """
        # get_data_list = []
        # docs = db.collection(self.collection_name).where("taught", "!=", taught).order_by(
        #     u'updated_at', direction=firestore.Query.ASCENDING).limit(limit).stream()
        # for doc in docs:
        #     word_dict = doc.to_dict()
        #     get_data_list.append({
        #         "word": word_dict["word"],
        #         "mean": word_dict["word"],
        #         "tag_list": word_dict["tag_list"],
        #     })
        get = False

        word_cnt = system_service.get_system_data()["word_cnt"]
        random_index = random.randint(0, word_cnt-1)

        for i in range(limit):
            docs = db.collection(self.collection_name).where(
                "index", "==", random_index).limit(1).get()
            if docs:
                word_dict = docs[0].to_dict()
                if word_dict["kind"] == "NG":
                    pass
                elif "taught" in word_dict:
                    if word_dict["taught"] != taught:
                        get = True
                        break
                else:
                    get = True
                    break
            random_index = (random_index + 1) % word_cnt
            
        if not get:
            docs = db.collection(self.collection_name).where(
                "word", "==", "むーちゃん").limit(1).get()

        if get_ref:
            return docs[0]._reference
        return models.WordAll(**docs[0].to_dict())

    def update_mean(self, word: str, mean: str, taught: str):
        """ 意味書き換え
        """
        docs = db.collection(self.collection_name).where(
            "word", "==", word).limit(1).get()
        if docs:
            if docs[0].to_dict()["mean"] == mean:
                return False
            else:
                docs[0]._reference.set({
                    "mean": mean,
                    "taught": taught,
                    "updated_at": datetime.now(),
                    "cnt": firestore.Increment(1),
                    "kind": "",
                }, merge=True)
                return True
        return False

    def update_kind(self, word: str, kind: str):
        """ 種別書き換え
        """
        docs = db.collection(self.collection_name).where(
            "word", "==", word).limit(1).get()
        if docs:
            docs[0]._reference.set({
                "kind": kind,
                "updated_at": datetime.now(),
                "cnt": firestore.Increment(1),
            }, merge=True)
            return True
        return False

    def add_good(self, word: str):
        """ good加算
        """
        docs = db.collection(self.collection_name).where(
            "word", "==", word).limit(1).get()
        if docs:
            docs[0]._reference.set({
                "good": firestore.Increment(1),
                "updated_at": datetime.now(),
                "cnt": firestore.Increment(1),
            }, merge=True)
            return True
        return False

    def add_bad(self, word: str):
        """ bad加算
        """
        docs = db.collection(self.collection_name).where(
            "word", "==", word).limit(1).get()
        if docs:
            docs[0]._reference.set({
                "bad": firestore.Increment(1),
                "updated_at": datetime.now(),
                "cnt": firestore.Increment(1),
            }, merge=True)
            return True
        return False

    def add_tag(self, word: str, tag: str):
        """ タグ追加
        """            
        tag_data = tag_service.get_tag(tag)
        if tag_data:
            docs = db.collection(self.collection_name).where(
                "word", "==", word).limit(1).get()

            if docs:
                set_data = {
                    "tags": firestore.ArrayUnion([tag_data["text"]]),
                    "tags_cnt": {
                        tag_data["text"]: firestore.Increment(1)
                    },
                    "updated_at": datetime.now(),
                    "cnt": firestore.Increment(1),
                }
                # 初めてのタグはlikeに計算
                if tag_data["text"] not in docs[0].to_dict()["tags"]:
                    set_data["like"] = firestore.Increment(tag_data["pnt"])

                docs[0]._reference.set(set_data, merge=True)
                return True

        return False

    def update_tags(self, word: str, tags_cnt: dict):
        """ タグ追加
        """
        tags = []
        like = 0
        
        # print(tags_cnt)
        # return
        
        for key in tags_cnt:
            tag_data = tag_service.get_tag(key)

            if tag_data:
                tags.append(tag_data["text"])
                like = like + tag_data["pnt"]
        
        docs = db.collection(self.collection_name).where(
            "word", "==", word).limit(1).get()

        if docs:
            set_data = {
                "tags": firestore.DELETE_FIELD,
                "tags_cnt": firestore.DELETE_FIELD,
            }
            docs[0]._reference.update(set_data)
            set_data = {
                "tags": tags,
                "tags_cnt": tags_cnt,
                "updated_at": datetime.now(),
                "cnt": firestore.Increment(1),
                "like": like,
            }
            docs[0]._reference.set(set_data, merge=True)
            return True
        else:
            print("失敗")

        return False
    
    def add_tag_for_text(self, word: str, text: str):
        """ 文章内からタグ追加
            タグ一覧を返す
        """
        retData = self.get_knowns_list(mean=text, teach_word=word)
        for tag in retData["tags"]:
            self.add_tag(word, tag["text"])

        return retData["tags"]

    def get_session(self, session_id: str):
        """ セッションID取得
            ヘッダーのsession_idパラメータに値が入っていない場合は新規idを発行
        """
        sessions = db.collection(self.collection_session)
        if not session_id:
            session_id = str(uuid4())
            doc_ref = sessions.document(document_id=session_id)
            data = {}
            data["created_at"] = datetime.now()
            doc_ref.set(data)
            system_service.add_session()

        return session_id

    def time_test(self):
        LIMIT_CNT = 60
        tweet_cnt = system_service.get_tweet_cnt()
        if tweet_cnt <= LIMIT_CNT:
            dt_now = datetime.now()
            system_service.add_tweet_cnt()
            if tweet_cnt == LIMIT_CNT:
                nokori = 60 - dt_now.minute
                if 0 < nokori:
                    print("いっぱいお話ししてちょっと疲れたの。\n{}分くらい休憩するの。".format(nokori))

    def post_tweet(self, msg):
        """ ツイートする
        """
        LIMIT_CNT = 95
        ret = {}
        ret["state"] = ""
        ret["id"] = ""
        tweet_cnt = system_service.get_tweet_cnt()
        
        if tweet_cnt > LIMIT_CNT:
            ret["state"] = "limit"
        else:
            status = tweet_api.update_status(msg)
            system_service.add_tweet_cnt()
            ret["state"] = "tweet"
            ret["id"] = status.id
            if tweet_cnt == LIMIT_CNT:
                dt_now = datetime.now()
                nokori = 60 - dt_now.minute
                if 0 < nokori:
                    tweet_api.update_status(
                        "いっぱいお話ししてちょっと疲れたの。\n{}分くらい休憩するの。".format(nokori))

        return ret

    def delete_tweet(self, id):
        """ ツイート削除する
        """
        try:
            # ツイートを消去
            tweet_api.destroy_status(id)
            return True
        except:
            return False

    def trend_tweet_force(self, trend_word: str):
        """ 指定したトレンドワードをツイートする
        """
        self.get_knowns_list(mean=trend_word)
        # 内容を保存
        id = self.create_temp(trend_word.replace("#", ""), "意味")
        msg = ("最近「{}」って言葉をよく耳にするよ！\n"
               "でも、むーちゃんは何の事かよく分かんない。\n"
               "だれか教えにきて欲しいな。\n"
               "https://torichan.app/ext/{}").format(
            trend_word, id)
               
        tweet_id = ""
        state = ""

        # ツイートする
        ret = self.post_tweet(msg)
        tweet_id = ret["id"]
        state = ret["state"]
            
        self.add_tweet_log(tweet_id, msg, state)

    def trend_tweet(self):
        """ ツイッタートレンドからランダムでピックアップしてツイートする
        """
        # 日本のWOEID
        woeid = 23424856
        # トレンド取得
        trends = tweet_api.trends_place(woeid)[0]

        msg = ""
        for i in range(50):
            # ローマ字のみの判定用
            re_roma = re.compile(r'^[a-zA-Z0-9_]+$')  # a-z:小文字、A-Z:大文字
            # トレンドワードからランダムで取得
            trend_word = random.choice(trends["trends"])["name"]

            # ローマ字のみは除外
            if re_roma.fullmatch(trend_word):
                pass
            else:
                # ツイート内容の生成
                ret_data = self.get_knowns_list(mean=trend_word)
                if ret_data["unknown"] and trend_word != ret_data["unknown"]["word"]:
                    # 内容を保存
                    id = self.create_temp(
                        ret_data["unknown"]["word"].replace("#", ""), "意味")
                    msg = ("最近「{}」って言葉をよく耳にするよ！\n"
                            "でも「{}」がどういう意味かわかんない。\n"
                            "だれか教えにきて欲しいな。\n"
                            "https://torichan.app/ext/{}").format(
                                trend_word, ret_data["unknown"]["word"], id)
                elif ret_data["known"] and not ret_data["unknown"]:
                    msg = ("最近「{}」って言葉をよく耳にするよ！\n"
                            "むーちゃん「{}」って言葉は知ってるよ！\n"
                            "いっぱい色んな言葉を教えて欲しいな。\n"
                            "https://torichan.app").format(
                                trend_word, ret_data["unknown"]["word"])
                else:
                    # 内容を保存
                    id = self.create_temp(trend_word.replace("#", ""), "意味")
                    msg = ("最近「{}」って言葉をよく耳にするよ！\n"
                            "でも、むーちゃんは何の事かよく分かんない。\n"
                            "だれか教えにきて欲しいな。\n"
                            "https://torichan.app/ext/{}").format(
                                trend_word, id)
                break
            
            # # NGワードチェック
            # elif not self.ng_word_check(trend_word, 3):
            #     # ツイート内容の生成
            #     ret_data = self.get_knowns_list(mean=trend_word)
            #     if ret_data["unknown"] and trend_word != ret_data["unknown"]["word"]:
            #         # 内容を保存
            #         id = self.create_temp(
            #             ret_data["unknown"]["word"].replace("#", ""), "意味")
            #         msg = ("最近「{}」って言葉をよく耳にするよ！\n"
            #                "でも「{}」がどういう意味かわかんない。\n"
            #                "だれか教えにきて欲しいな。\n"
            #                "https://torichan.app/ext/{}").format(
            #                    trend_word, ret_data["unknown"]["word"], id)
            #     elif ret_data["known"] and not ret_data["unknown"]:
            #         msg = ("最近「{}」って言葉をよく耳にするよ！\n"
            #                "むーちゃん「{}」って言葉は知ってるよ！\n"
            #                "いっぱい色んな言葉を教えて欲しいな。\n"
            #                "https://torichan.app").format(
            #                    trend_word, ret_data["unknown"]["word"])
            #     else:
            #         # 内容を保存
            #         id = self.create_temp(trend_word.replace("#", ""), "意味")
            #         msg = ("最近「{}」って言葉をよく耳にするよ！\n"
            #                "でも、むーちゃんは何の事かよく分かんない。\n"
            #                "だれか教えにきて欲しいな。\n"
            #                "https://torichan.app/ext/{}").format(
            #                    trend_word, id)
            #     break

        tweet_id = ""
        state = ""

        # ツイートする
        state = self.ng_check(trend_word)
        if state == "":
            ret = self.post_tweet(msg)
            tweet_id = ret["id"]
            state = ret["state"]
            
        self.add_tweet_log(tweet_id, msg, state)
        

    def ng_word_check(self, word, limit=3):
        """ 指定したワードが不適切な単語かチェックする
            wordで検索したツイート20件の中にNGワードが一定数含まれているかチェック
            limitで指定した数ヒットしたらTrueを返す
        """
        ng_word_hit = 0
        for tweet in tweepy.Cursor(tweet_api.search, q=word, result_type="popular").items(20):
            for ng_word in self.ng_list:
                if ng_word in tweet.text:
                    ng_word_hit = ng_word_hit + 1
                    break

            if ng_word_hit >= limit:
                return True

        return False

    def check_text_conv(self, text):
        """ テキスト内にNGワード入っていないかチェックする
        """
        check_text = ''.join(text.split())
        check_text = check_text.lower()
        check_text = jaconv.h2z(check_text, kana=True, digit=False, ascii=False)
        check_text = jaconv.z2h(check_text, kana=False, digit=True, ascii=True)
        check_text = jaconv.kata2hira(check_text)
        return check_text
    
    def ng_text_check2(self, text):
        """ テキスト内にNGワード入っていないかチェックする
        """
        check_text = self.check_text_conv(text)
        # 正規表現のチェック
        for ng_regex in self.ng_regex:
            if re.match(ng_regex, check_text):
                return True
        return False
    
    def ng_text_check(self, text):
        """ テキスト内にNGワード入っていないかチェックする
        """
        check_text = self.check_text_conv(text)
        # 7文字以上の数字はNG        
        if len(re.sub(r'\D', '', text)) >= 7:
            return True
        # 正規表現のチェック
        for ng_regex in self.ng_regex:
            if re.match(ng_regex, check_text):
                return True
        # 部分一致のチェック
        for ng_word in self.ng_list:
            if ng_word in check_text:
                return True
        return False

    def ng_ip_check(self, ip_address: str):
        """ IPアドレスがにNG_IPに入っていないかチェックする
        """
        check_ip_address = ''.join(ip_address.split())
        for ng_ip in self.ng_ip:
            if ng_ip == check_ip_address:
                return True
        return False
    
    def ng_session_check(self, session_id: str):
        """ セッションIDがにNG_リストに入っていないかチェックする
        """
        check_session_id = ''.join(session_id.split())
        for ng_session in self.ng_session:
            if ng_session == check_session_id:
                return True
        return False

    def ng_check(self, msg: str, ip_address: str="", session_id: str=""):
        """ セッションIDがにNG_リストに入っていないかチェックする
        """
        ret = ""
        if self.ng_session_check(session_id):
            ret = "ng_session"
        elif ip_address and self.ng_ip_check(ip_address):
            ret = "ng_ip"
        elif session_id and self.ng_text_check(msg):
            ret = "ng_text"
        
        if self.ng_text_check2(msg):
            ret = "ng_text2"
        return ret
    
    def mean_update_tweet(self, word_ref, session_id: str, ip_address: str):
        """ 覚えたワードについてツイートする
        """
        word_data = word_ref.get().to_dict()
        msg = ""
        tweet_id = ""
        state = ""
        data = {}
        # ツイート内容生成
        msg = ("「{}」の意味を勘違いしてたの！\n"
               "ほんとは「{}」のことだよ！").format(word_data["word"], word_data["mean"])
        
        state = self.ng_check(word_data["word"], ip_address, session_id)
        if not state:
            state = self.ng_check(word_data["mean"], ip_address, session_id)
            
        if state == "ng_session" or state == "ng_ip" or state == "ng_text":
            data["kind"] = "NG"
            word_ref.update(data)
        elif state == "ng_text2":
            data["kind"] = "NG"
            word_ref.update(data)
            system_service.add_ng_session(session_id)
            self.renew_ng_list()
        else:
            ret = self.post_tweet(msg)
            state = ret["state"]
            tweet_id = ret["id"]
            if ret["state"] == "tweet":
                # ツイートしたワードの情報更新
                data["tweeted_at"] = datetime.now()
                data["updated_at"] = datetime.now()
                data["kind"] = ""
                word_ref.update(data)
            
        ret["tweet_log"] = self.add_tweet_log(tweet_id, msg, state)

        return ret

    def word_create_tweet(self, word_ref, tag: str, session_id: str, ip_address: str):
        """ 覚えたワードについてツイートする
        """
        word_data = word_ref.get().to_dict()
        msg = ""
        tweet_id = ""
        state = ""
        data = {}
        # ツイート内容生成
        msg = ("今「{}」って言葉を教えてもらったの！\n"
               "「{}」のことだよ！").format(word_data["word"], word_data["mean"])

        if tag:
            tag_data = tag_service.get_tag(tag)
            if tag_data:
                if tag_data["part"] == "形容詞":
                    msg = (msg +
                           "\nあと「{}」は{}んだよ！").format(word_data["word"], tag_data["text"])
                elif tag_data["part"] == "形容動詞":
                    msg = (msg +
                           "\nあと「{}」は{}なんだよ！").format(word_data["word"], tag_data["text"])


        state = self.ng_check(word_data["word"], ip_address, session_id)
        if not state:
            state = self.ng_check(word_data["mean"], ip_address, session_id)
            
        if state == "ng_session" or state == "ng_ip" or state == "ng_text":
            data["kind"] = "NG"
            word_ref.update(data)
        elif state == "ng_text2":
            data["kind"] = "NG"
            word_ref.update(data)
            system_service.add_ng_session(session_id)
            self.renew_ng_list()
        else:
            ret = self.post_tweet(msg)
            state = ret["state"]
            tweet_id = ret["id"]
            if ret["state"] == "tweet":
                # ツイートしたワードの情報更新
                data["tweeted_at"] = datetime.now()
                data["updated_at"] = datetime.now()
                data["kind"] = ""
                word_ref.update(data)
            
        ret["tweet_log"] = self.add_tweet_log(tweet_id, msg, state)

        return ret

    def remembered_tweet(self):
        """ 直近で覚えたワードについてツイートする
        """
        docs = db.collection(self.collection_name).order_by(
            u'created_at', direction=firestore.Query.DESCENDING).limit(1).stream()

        for doc in docs:
            doc_dict = doc.to_dict()

        if not doc_dict:
            print("remembered_tweet faild")
            return
        
        if doc_dict["kind"] == "NG":
            print("remembered_tweet NG1")
            return

        if not self.ng_text_check(doc_dict["word"]):
            # ツイート内容生成
            msg = ("今「{}」って言葉を教えてもらったの！\n"
                   "「{}」のことだよ！").format(doc_dict["word"], doc_dict["mean"])
            # ツイートしたワードの情報更新
            data = {}
            data["tweeted_at"] = datetime.now()
            data["updated_at"] = datetime.now()
            doc._reference.update(data)
            # ツイート
            ret = self.post_tweet(msg)
            self.add_tweet_log(ret["id"], msg, ret["state"])
            
        else:
            print("remembered_tweet NG2")

    def word_tag_add_tweet(self, word: str, tag: str):
        """ タグ追加についてツイートする
        """
        msg = ""
        tag_data = tag_service.get_tag(tag)
        if tag_data:
            if tag_data["part"] == "形容詞":
                msg = ("{}は{}んだって！").format(word, tag)
            elif tag_data["part"] == "形容動詞":
                msg = ("{}は{}なんだって！").format(word, tag)

        tweet_id = ""
        state = ""

        if msg:
            # ツイートする
            state = self.ng_check(word)

            if state == "":
                ret = self.post_tweet(msg)
                tweet_id = ret["id"]
                state = ret["state"]
                
            self.add_tweet_log(tweet_id, msg, state)
            return msg
        return

    def word_relation_tag_tweet(self):
        """ タグ追加についてツイートする
        """
        msg = ""
        tweet_id = ""
        state = ""
        tag = tag_service.get_random_tag_more0()

        word1 = self.get_common_tag_word(word="", tag=tag["text"])
        if word1:
            word2 = self.get_common_tag_word(word=word1.word, tag=tag["text"])
            state = self.ng_check(word1.word)
            
            if word2:
                if not state:
                    state = self.ng_check(word2.word)

                if tag["part"] == "形容詞":
                    # 内容を保存
                    id = self.create_temp(tag["text"], "形容詞関連")
                    msg = ("{}や{}は{}んだよ。\n"
                        "{}ものをもっと教えてほしいな。\n"
                        "https://torichan.app/ext/{}").format(word1.word, word2.word, tag["text"], tag["text"], id)
                elif tag["part"] == "形容動詞":
                    # 内容を保存
                    id = self.create_temp(tag["text"], "形容動詞関連")
                    msg = ("{}や{}は{}なんだよ。\n"
                        "{}なものをもっと教えてほしいな。\n"
                        "https://torichan.app/ext/{}").format(word1.word, word2.word, tag["text"], tag["text"], id)

        if not msg:
            if tag["part"] == "形容詞":
                # 内容を保存
                id = self.create_temp(tag["text"], "形容詞関連")
                msg = ("{}ものが知りたいの。\n"
                       "誰か{}ものを教えに来てほしいな。\n"
                       "https://torichan.app/ext/{}").format(tag["text"], tag["text"], id)
            elif tag["part"] == "形容動詞":
                # 内容を保存
                id = self.create_temp(tag["text"], "形容動詞関連")
                msg = ("{}なものが知りたいの。\n"
                       "誰か{}なものを教えに来てほしいな。\n"
                       "https://torichan.app/ext/{}").format(tag["text"], tag["text"], id)

        if msg:
            if state == "":
                ret = self.post_tweet(msg)
                tweet_id = ret["id"]
                state = ret["state"]
                
            self.add_tweet_log(tweet_id, msg, state)
            return msg
        else:
            return

    def known_word_tweet(self):
        """ 知っているワードについてツイートする
        """
        # ツイートするワードのピックアップ
        ref = self.get_topic_word(get_ref=True)
        doc_dict = ref.get().to_dict()
        # ツイート内容生成
        msg = ("むーちゃんは「{}」って言葉を知ってるよ！\n"
               "「{}」のことだよ！").format(doc_dict["word"], doc_dict["mean"])
        # ツイートしたワードの情報更新
        data = {}
        data["tweeted_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        ref.update(data)
        
        tweet_id = ""
        state = ""
        # ツイート
        state = self.ng_check(doc_dict["word"])
        if not state:
            state = self.ng_check(doc_dict["mean"])
        
        if state == "":
            ret = self.post_tweet(msg)
            tweet_id = ret["id"]
            state = ret["state"]
        
        self.add_tweet_log(tweet_id, msg, state)

    def unknown_word_tweet(self):
        """ 意味を知らないワードについてツイートする
        """
        # 意味を知らないワードのピックアップ
        data = self.get_topic_unknown()
        # 内容を保存
        id = self.create_temp(data["word"], "意味")

        # ツイート内容生成
        msg = ("「{}」ってどういう意味かな？\n"
               "最近きいたんだけど、意味は知らないの。\n"
               "だれか教えにきて欲しいな。\n"
               "https://torichan.app/ext/{}").format(data["word"], id)

        tweet_id = ""
        state = ""
        # ツイート
        state = self.ng_check(data["word"])
        
        if state == "":
            ret = self.post_tweet(msg)
            tweet_id = ret["id"]
            state = ret["state"]
        
        self.add_tweet_log(tweet_id, msg, state)

    def janken_tweet(self):
        """ じゃんけん結果のツイートする
        """
        # 当日のじゃんけん結果を取得
        data = system_service.get_janken_result_today()

        if data["win_cnt"] + data["lose_cnt"] > 0:
            if data["win_cnt"] < data["lose_cnt"]:
                # ツイート内容生成
                msg = ("今日はじゃんけんで遊んでもらえたの！\n"
                       "{}勝{}敗でむーちゃんが勝ってたよ！\n"
                       "またじゃんけんしにきて欲しいな！\n"
                       "https://torichan.app/ext/janken").format(data["lose_cnt"], data["win_cnt"])
            elif data["win_cnt"] > data["lose_cnt"]:
                # ツイート内容生成
                msg = ("今日はじゃんけんで遊んでもらえたの！\n"
                       "{}勝{}敗でむーちゃんが負けてたの。\n"
                       "次は勝ちたいの！\n"
                       "https://torichan.app/ext/janken").format(data["lose_cnt"], data["win_cnt"])
            else:
                # ツイート内容生成
                msg = ("今日はじゃんけんで遊んでもらえたの！\n"
                       "{}勝{}敗でいい勝負だったよ。\n"
                       "次は勝ちたいの！\n"
                       "https://torichan.app/ext/janken").format(data["lose_cnt"], data["win_cnt"])
        else:
            # ツイート内容生成
            msg = ("じゃんけんしたいな～。\n"
                   "誰かじゃんけんしに来てほしいな！\n"
                   "https://torichan.app/ext/janken")

        # ツイート
        ret = self.post_tweet(msg)
        self.add_tweet_log(ret["id"], msg, ret["state"])

    def follow_back(self):
        """ フォローバック処理
        """
        # フォロワーのアカウントデータを取得
        follower_list = tweet_api.followers(count=50)
        for follower in follower_list:
            if not follower.following:
                if not follower.protected:
                    tweet_api.create_friendship(follower.id)
                else:
                    # 鍵垢はしない
                    pass
            else:
                # フォロー済み
                pass

    def create_temp(self, word: str, kind: str, maen: str = "", set_id: str = ""):
        """ テンポラリに情報を保存
        """
        doc = db.collection(self.collection_temporary).document()
        doc.set({
            "cnt": 0,
            "kind": kind,
            "word": word,
            "mean": maen,
            "id": set_id,
            "created_at": datetime.now()
        }
        )
        return doc.id

    def create_temp_remember_word(self, word: str):
        """ 覚えた単語の情報をテンポラリに保存
        """
        data = self.get(word)
        id = self.create_temp(word, "覚えた単語", data.mean)
        return id

    def create_temp_fromt(self, word: str, set_id: str):
        """ フロント側から情報をテンポラリに保存
        """
        data = self.get(word)
        id = self.create_temp(word, "覚えた単語", data.mean, set_id)
        return id

    def get_temp(self, id: str):
        """ テンポラリから情報を取得
        """
        doc = db.collection(self.collection_temporary).document(id).get()
        if doc.exists:
            return doc.to_dict()
        return

    def get_temp_front(self, id: str):
        """ テンポラリから情報を取得
        """
        docs = db.collection(self.collection_temporary).where(
            "id", "==", id).limit(1).get()
        if docs and docs[0].exists:
            return docs[0].to_dict()
        return

    def get_one_day_learn_words(self, year: int, month: int, day: int):
        print("{}/{}/{}".format(year, month, day))
        docs = db.collection(self.collection_name).where(
            "updated_at", ">=", datetime(year, month, day, 0, 0, 0)).where(
                "updated_at", "<=", datetime(year, month, day, 23, 59, 59)).limit(50).get()

        word_list = []
        for doc in docs:
            word_list.append(doc.to_dict())

        return word_list



    def add_tweet_log(self, tweet_id: str, message: str, state: str):
        doc = db.collection(self.collection_tweet_log).document()
        doc.set({
            "tweet_id": tweet_id,
            "message": message,
            "state": state,
            "action": "create",
            "created_at": datetime.now()
        })

        return str(doc.id)


    def tweet_delete(self, ref: str):
        doc_ref = db.collection(self.collection_tweet_log).document(ref)
        log_data = doc_ref.get().to_dict()
        
        if log_data["tweet_id"] != "":
            self.delete_tweet(log_data["tweet_id"])
            data = {
                "tweet_id": "",
                "action": "tweet_delete",
            }
            doc_ref.update(data)


    def tweet_force(self, ref: str):
        doc_ref = db.collection(self.collection_tweet_log).document(ref)
        log_data = doc_ref.get().to_dict()
    
        ret = self.post_tweet(log_data["message"], "admin", "admin", False)
        data = {
            "tweet_id": ret["id"],
            "action": "tweet_force",
        }
        doc_ref.update(data)

    
    def get_tweet_log(self, ref: str):
        doc_ref = db.collection(self.collection_tweet_log).document(ref)
        log_data = doc_ref.get().to_dict()
        return log_data
    
    
    def get_tweet_log_next(self, limit: int, next_key=None):
        doc_dict_list = []
        ref_list = []

        if next_key:
            docs = db.collection(self.collection_tweet_log).order_by(
                u'created_at', direction=firestore.Query.DESCENDING).start_after({u'created_at': next_key}).limit(limit).stream()

            for doc in docs:
                doc_dict_list.append(doc.to_dict())
                ref_list.append(str(doc.id))

        else:
            docs = db.collection(self.collection_tweet_log).order_by(
                u'created_at', direction=firestore.Query.DESCENDING).limit(limit).stream()

            for doc in docs:
                doc_dict_list.append(doc.to_dict())
                ref_list.append(str(doc.id))
        
        
        for word_data in doc_dict_list:
            for key, value in word_data.items():
                if isinstance(value, (DatetimeWithNanoseconds)):
                    print(value)
                    word_data[key] = str(value)


        next = doc_dict_list[-1]['created_at']
        
        ret = {"doc": doc_dict_list, "ref": ref_list, "next_key": next, "now_key": next_key}

        return ret


word_instance = WordService()
