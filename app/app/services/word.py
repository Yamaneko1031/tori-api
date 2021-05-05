import os
import random
import logging
from uuid import uuid4
from datetime import datetime
from typing import List
import re

import tweepy
from google.cloud.firestore_v1.transaction import Transaction
from google.cloud import firestore
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
    collection_name = "words"
    collection_unknown = "unknowns"
    collection_session = "sessions"
    collection_temporary = "temporaries"

    def __init__(self):
        """ コンストラクタ
        """
        # NGリスト取得
        self.ng_list = system_service.get_ng_list()
        print(self)
        # print(self.ng_list)

    def create(self, word_create: models.WordCreate, taught: str) -> models.WordAll:
        """ 新規単語の追加
        """
        retData = self.get_knowns_list(
            mean=word_create.mean, teach_word=word_create.word, secret_tag=word_create.secret_tag)

        docs = db.collection(self.collection_name).where(
            "word", "==", word_create.word).limit(1).get()
        if docs:
            if self.update_mean(word_create.word, word_create.mean, taught):
                self.mean_update_tweet(docs[0]._reference)
            ref = docs[0]._reference
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
            self.word_create_tweet(ref, word_create.secret_tag)

        retData["create"] = models.WordAll(**ref.get().to_dict())

        return retData

    def delete(self, word: str):
        """ 単語情報削除
        """
        docs = db.collection(self.collection_name).where(
            "word", "==", word).limit(1).get()
        for doc in docs:
            doc._reference.delete()
        return

    def get(self, word: str) -> models.WordAll:
        """ 単語情報取得
        """
        docs = db.collection(self.collection_name).where(
            "word", "==", word).limit(1).get()
        if docs:
            return models.WordAll(**docs[0].to_dict())
        return

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

    def get_topic_unknown(self, limit: int = 10):
        """ 意味を知らない単語の中から一つピックアップして取得
        """
        get_data_list = []
        docs = db.collection(self.collection_unknown).order_by(
            u'interest', direction=firestore.Query.DESCENDING).limit(limit).stream()

        for doc in docs:
            unknown = doc.to_dict()
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

        word_cnt = system_service.get_system_data()["word_cnt"]
        random_index = random.randint(0, word_cnt-1)

        for i in range(limit):
            docs = db.collection(self.collection_name).where(
                "index", "==", random_index).limit(1).get()
            if docs:
                word_dict = docs[0].to_dict()
                if self.ng_text_check(word_dict["word"]):
                    pass
                elif self.ng_text_check(word_dict["mean"]):
                    pass
                elif "taught" in word_dict:
                    if word_dict["taught"] != taught:
                        break
                else:
                    break
            random_index = (random_index + 1) % word_cnt

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
                    "updated_at": datetime.utcnow(),
                    "cnt": firestore.Increment(1),
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
                "updated_at": datetime.utcnow(),
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
                "updated_at": datetime.utcnow(),
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
                "updated_at": datetime.utcnow(),
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
                    "updated_at": datetime.utcnow(),
                    "cnt": firestore.Increment(1),
                }
                # 初めてのタグはlikeに計算
                if tag_data["text"] not in docs[0].to_dict()["tags"]:
                    set_data["like"] = firestore.Increment(tag_data["pnt"])

                docs[0]._reference.set(set_data, merge=True)
                return True

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
            data["created_at"] = datetime.utcnow()
            doc_ref.set(data)
            system_service.add_session()

        return session_id

    def post_tweet(self, msg):
        """ ツイートする
        """
        if not self.ng_text_check(msg):
            tweet_api.update_status(msg)

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

        # ツイートする
        self.post_tweet(msg)

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
            # NGワードチェック
            elif not self.ng_word_check(trend_word, 3):
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

        # ツイートする
        if msg:
            # print(msg)
            self.post_tweet(msg)

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

    def ng_text_check(self, text):
        """ テキスト内にNGワード入っていないかチェックする
        """
        for ng_word in self.ng_list:
            if ng_word in text:
                return True
        return False

    def mean_update_tweet(self, word_ref):
        """ 覚えたワードについてツイートする
        """
        word_data = word_ref.get().to_dict()

        if not self.ng_word_check(word_data["word"]):
            msg = ""
            data = {}
            # ツイート内容生成
            msg = ("「{}」の意味を勘違いしてたの！\n"
                   "ほんとは「{}」のことだよ！").format(word_data["word"], word_data["mean"])

            # ツイートしたワードの情報更新
            data["tweeted_at"] = datetime.utcnow()
            data["updated_at"] = datetime.utcnow()
            word_ref.update(data)
            # ツイート
            self.post_tweet(msg)
        else:
            print("remembered_tweet ng word")

    def word_create_tweet(self, word_ref, tag: str):
        """ 覚えたワードについてツイートする
        """
        word_data = word_ref.get().to_dict()

        if not self.ng_word_check(word_data["word"]):
            msg = ""
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

            # ツイートしたワードの情報更新
            data["tweeted_at"] = datetime.utcnow()
            data["updated_at"] = datetime.utcnow()
            word_ref.update(data)
            # ツイート
            self.post_tweet(msg)
        else:
            print("remembered_tweet ng word")

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

        if not self.ng_word_check(doc_dict["word"]):
            # ツイート内容生成
            msg = ("今「{}」って言葉を教えてもらったの！\n"
                   "「{}」のことだよ！").format(doc_dict["word"], doc_dict["mean"])
            # ツイートしたワードの情報更新
            data = {}
            data["tweeted_at"] = datetime.utcnow()
            data["updated_at"] = datetime.utcnow()
            doc._reference.update(data)
            # ツイート
            self.post_tweet(msg)
        else:
            print("remembered_tweet ng word")

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

        if msg:
            self.post_tweet(msg)
            return msg
        else:
            return

    def word_relation_tag_tweet(self):
        """ タグ追加についてツイートする
        """
        msg = ""
        tag = tag_service.get_random_tag_more0()

        word1 = self.get_common_tag_word(word="", tag=tag["text"])
        if word1:
            word2 = self.get_common_tag_word(word=word1.word, tag=tag["text"])
            if word2:
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
            self.post_tweet(msg)
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
        data["tweeted_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        ref.update(data)
        # ツイート
        self.post_tweet(msg)

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

        # ツイート
        self.post_tweet(msg)

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
                       "またじゃんけんしきて欲しいな！\n"
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
        self.post_tweet(msg)

    def create_temp(self, word: str, kind: str):
        """ テンポラリに情報を保存
        """
        doc = db.collection(self.collection_temporary).document()
        doc.set({
            "cnt": 0,
            "kind": kind,
            "word": word,
            "created_at": datetime.utcnow()
        }
        )
        return doc.id

    def get_temp(self, id: str):
        """ テンポラリから情報を取得
        """
        doc = db.collection(self.collection_temporary).document(id).get()
        if doc.exists:
            return doc.to_dict()
        return


word_instance = WordService()
