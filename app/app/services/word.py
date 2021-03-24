import os
import logging
import random
from datetime import datetime
from typing import List
from uuid import uuid4

from google.cloud import firestore
from google.cloud.firestore_v1.transaction import Transaction
import tweepy

from app import models
from app.util import morpheme

db = firestore.Client()
logger = logging.getLogger(__name__)

auth = tweepy.OAuthHandler(
    os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'],
                      os.environ['ACCESS_TOKEN_SECRET'])

tweet_api = tweepy.API(auth)

NEGATIVE_WORD_LIST = (
    "死",
    "ﾀﾋ",
    "タヒ",
    "他界",
    "亡く",
    "成仏",
    "逝去",
    "老衰",
    "絶命",
    "不幸",
    "先立",
    "訃報"
    "冥福"
    "遺体"
    "葬",
    "殺",
    "命の火",
    "息の根",
    "息を引",
    "がん",
    "末期",
    "病",
    "犯",
    "罪",
    "薬",
    "違法",
    "違反",
    "逮捕",
    "鬱",
    "うつ",
    "苦",
    "暴",
    "殴",
    "痛",
    "絶望",
)


@firestore.transactional
def create_tr(transaction: Transaction, word_create: models.WordCreate, taught: str,
              colect_word: str, colect_unknown: str, colect_session: str
              ):
    """ 新規単語の追加で呼び出すトランザクション処理
    """
    # unknownsコレクションにある場合は削除する
    docs = db.collection(colect_unknown).where(
        "word", "==", word_create.word).stream()
    for doc in docs:
        transaction.delete(doc._reference)

    # wordsコレクションに追加
    word_data = models.WordAll(**word_create.dict()).dict()
    word_data["taught"] = taught
    word_ref = db.collection(colect_word).document()
    transaction.set(word_ref, word_data)

    # sessionsコレクション更新
    session_ref = db.collection(
        colect_session).document(document_id=taught)
    session_data = {
        "teach_words": firestore.ArrayUnion([word_create.word]),
        "teach_Refs": firestore.ArrayUnion([word_ref]),
        "teach_cnt": firestore.Increment(1),
    }
    transaction.set(session_ref, session_data, merge=True)

    return word_ref


class WordService:
    collection_name = "words"
    collection_unknown = "unknowns"
    collection_session = "sessions"

    def create(self, word_create: models.WordCreate, taught: str) -> models.WordAll:
        """ 新規単語の追加
        """
        transaction = db.transaction()
        ref = create_tr(transaction=transaction,
                        word_create=word_create,
                        taught=taught,
                        colect_word=self.collection_name,
                        colect_unknown=self.collection_unknown,
                        colect_session=self.collection_session
                        )
        return models.WordAll(**ref.get().to_dict())

    def get(self, word: str) -> models.WordAll:
        """ 単語情報取得
        """
        docs = db.collection(self.collection_name).where(
            "word", "==", word).limit(1).get()
        if docs[0].exists:
            return models.WordAll(**docs[0].to_dict())
        return

    def get_knowns_list(self, mean: str, teach_word: str = ""):
        """ 意味を分解して知ってる単語、知らない単語に分ける
            知らない単語はDBに追加される
            知っている単語、知らない単語の中からランダムで一つ選んで返す
        """
        # 意味の中から認識可能な単語を取得
        phrase_list = morpheme.disassemble(mean)

        word_ref = ""
        trend_word = ""

        # teach_wordに値が入っている場合は参照情報を保存する
        if teach_word:
            # 教えた単語の参照情報を取得
            docs = db.collection(self.collection_name).where(
                "word", "==", teach_word).limit(1).stream()

            if docs:
                for doc in docs:
                    word_ref = doc._reference
        # teach_wordに値が入って無い場合は入力ワードをトレンド情報に保存する
        else:
            trend_word = mean

        # 知っている単語、知らない単語の一覧を作成
        known_list = []
        unknown_list = []
        for key, value in phrase_list.items():
            docs = db.collection(self.collection_name).where(
                "word", "==", key).limit(1).get()
            if docs:
                known_list.append({"word": key, "kind": value})
            else:
                unknown_list.append({"word": key, "kind": value})
                unknown_ref = db.collection(
                    self.collection_unknown).document()
                unknown_ref.set({
                    "word": key,
                    "kind": value,
                    "word_ref": word_ref,
                    "trend": trend_word,
                    "interest": firestore.Increment(1)
                }, merge=True)

        # 知っている単語、知らない単語の中からランダムで一つ選んで返す
        ret_data = {"known": 0, "unknown": 0}
        if known_list:
            ret_data["known"] = random.choice(known_list)
        if unknown_list:
            ret_data["unknown"] = random.choice(unknown_list)

        return ret_data

    def get_topic_taught(self, taught: str, limit: int = 10) -> models.WordAll:
        """ 教えた単語の中から一つピックアップして取得
        """
        doc = db.collection(self.collection_session).document(
            document_id=taught).get()
        ref = random.choice(doc.to_dict()["teach_refs"])
        return models.WordAll(**ref.get().to_dict())

    def get_topic_unknown(self, limit: int = 10):
        """ 意味を知らない単語の中から一つピックアップして取得
        """
        get_data_list = []
        docs = db.collection(self.collection_unknown).order_by(
            u'Interest', direction=firestore.Query.DESCENDING).limit(limit).stream()

        for doc in docs:
            unknown = doc.to_dict()
            ref = doc.to_dict()["word_ref"].get().to_dict()
            get_data_list.append({
                "word": unknown["word"],
                "kind": unknown["kind"],
                "ref": {
                    "word": ref["word"],
                    "mean": ref["mean"],
                }
            })

        return random.choice(get_data_list)

    def get_topic_word(self, taught: str, limit: int = 20) -> models.WordAll:
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

        get_data_list = []

        docs = db.collection(self.collection_name).order_by(
            'updated_at').stream()
        cnt = 0
        for doc in docs:
            word_dict = doc.to_dict()
            if "taught" in word_dict:
                if word_dict["taught"] != taught:
                    cnt = cnt + 1
                    get_data_list.append(doc._reference)
            if cnt >= limit:
                break

        ref = random.choice(get_data_list)
        return models.WordAll(**ref.get().to_dict())

    def update(self, word_update: models.WordUpdate, taught: str) -> models.WordAll:
        """ 単語情報更新
        """
        doc_ref = db.collection(
            self.collection_name).document(word_update.word)

        # パラメータを基に更新データ生成
        data = {}
        if word_update.mean != "":
            data["mean"] = word_update.mean
            data["taught"] = taught
        if word_update.raiting > 0:
            data["good"] = firestore.Increment(word_update.raiting)
        elif word_update.raiting < 0:
            data["bad"] = firestore.Increment(-word_update.raiting)
        data["tag_list"] = firestore.ArrayUnion(word_update.tag_list)
        data["updated_at"] = datetime.utcnow()

        doc_ref.update(data)
        doc = doc_ref.get()
        if doc.exists:
            return models.WordAll(**doc.to_dict())
        return

    def get_session(self, session_id: str):
        """ セッションID取得
            ヘッダーのsession_idパラメータに値が入っていない場合は新規idを発行
        """
        db = firestore.Client()
        sessions = db.collection(self.collection_session)
        if not session_id:
            session_id = str(uuid4())
            doc_ref = sessions.document(document_id=session_id)
            data = {}
            data["created_at"] = datetime.utcnow()
            doc_ref.set(data)

        return session_id

    # def delete(self, id: UUID) -> None:
    #     db.collection(self.collection_name).document(str(id)).delete()

    def post_tweet(self, msg):
        """ ツイートする
        """
        tweet_api.update_status(msg)

    def trend_tweet(self):
        """ ツイッタートレンドからランダムでピックアップしてツイートする
        """
        # 日本のWOEID
        woeid = 23424856
        # トレンド取得
        trends = tweet_api.trends_place(woeid)[0]

        msg = ""
        for i in range(10):
            # トレンドワードからランダムで取得
            trend_word = random.choice(trends["trends"])["name"]

            if not self.ng_word_check(trend_word):
                # ツイート内容の生成
                ret_data = self.get_knowns_list(mean=trend_word)
                if not ret_data["unknown"]:
                    msg = """最近「{}」って言葉をよく耳にするよ！\n 
                    ところで{}ってどういう意味なんだろう？\n
                    だれか教えにきて欲しいな！\n
                    https://torichan.app""".format(
                        trend_word, ret_data["unknown"])
                else:
                    msg = """最近「{}」って言葉をよく耳にするよ！\n
                    でも、むーちゃんは何の事かよく分かんない。\n
                    だれか教えにきて欲しいな！\n
                    https://torichan.app""".format(
                        trend_word)
                break

        # ツイートする
        if msg:
            print(msg)
            # self.post_tweet(msg)

    def ng_word_check(self, word, limit):
        """ 指定したワードが不適切な単語かチェックする
            wordで検索したツイート20件の中にNGワードが一定数含まれているかチェック
            limitで指定した数ヒットしたらTrueを返す
        """
        ng_word_hit = 0
        for tweet in tweepy.Cursor(tweet_api.search, q=word, result_type="popular").items(20):
            for ng_word in NEGATIVE_WORD_LIST:
                if ng_word in tweet.text:
                    ng_word_hit = ng_word_hit + 1
                    break

            if ng_word_hit >= limit:
                return True

        return False

    def remembered_tweet(self, word):
        """ 覚えたワードについてツイートする
        """

    def known_word_tweet(self):
        """ 知っているワードについてツイートする
        """

    def unknown_word_tweet(self):
        """ 意味を知らないワードについてツイートする
        """
