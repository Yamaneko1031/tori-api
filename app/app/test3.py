import sys
from datetime import datetime

sys.path.append('/app')

import models, services

from google.cloud import firestore

db = firestore.Client()

# tag_service = services.tag_instance

# tag_service.use_tag("こたつ","人気", 1)

# print(dt.strftime("%y/%m/%d %A %H:%M:%S"))
# d_today = datetime.today().strftime("%y-%m-%d")
# print(d_today)
# print(datetime.today())

# word_service = services.WordService()

# word_service.add_tag2("こたつ","幸せ")

# word_create = models.WordCreate(word="こたつ",mean="あったかい")
# word_service.create(word_create,"aaaaaaaaaa")

# word_service.remembered_tweet()

# system_service = services.SystemService()
# tag_service = services.TagService()
test = {
    "美味しい":5,
    "明るい":2,
    "暗い":-1,
    "新しい":1,
    "古い":-1,
    "温かい":2,
    "冷たい":0,
    "暖かい":2,
    "涼しい":1,
    "暑い":-1,
    "寒い":-1,
    "熱い":-1,
    "厚い":0,
    "薄い":0,
    "美しい":3,
    "醜い":-3,
    "大きい":2,
    "小さい":2,
    "重い":0,
    "軽い":0,
    "硬い":0,
    "柔らかい":2,
    "厳しい":-2,
    "優しい":2,
    "高い":2,
    "低い":0,
    "安い":0,
    "近い":0,
    "遠い":0,
    "強い":2,
    "弱い":-1,
    "長い":1,
    "短い":-1,
    "早い":0,
    "遅い":0,
    "速い":3,
    "広い":2,
    "狭い":-2,
    "太い":0,
    "細い":0,
    "難しい":-3,
    "易しい":2,
    "良い":4,
    "悪い":-4,
    "不味い":-5,
    "すごい":4,
    "偉い":2,
}

KEIDOU = {
    "便利":2,
    "不便":-1,
    "綺麗":3,
    "上品":2,
    "下品":-1,
    "なめらか":1,
    "のどか":1,
    "幸せ":4,
    "専門的":0,
    "にぎやか":1,
    "静か":1,
    "ステキ":3,
    "華やか":2,
    "壮大":1,
    "偉大":2,
    "爽やか":1,
    "有名":2,
    "人気":3,
    "特殊":0,
    "変":-1,
    "健康":1,
    "不思議":0,
    "危険":-2,
    "ぶきみ":-2,
}



# def use_tag1(word: str):
#     colection = db.collection("tags1")
#     doc_ref = colection.document(word)
#     doc_ref.update({
#         "used": firestore.Increment(1),
#         "updated_at": datetime.utcnow(),
#     })

# use_tag1("すごい")


# colection = db.collection(u'tags1')
# docs = colection.order_by("updated_at", direction=firestore.Query.DESCENDING).stream()
# data = []
# tmp = {}
# for doc in docs:
#     tmp = doc.to_dict()
#     del tmp["updated_at"], tmp["used"]
#     data.append(tmp)

# print(data)




# colection = db.collection("tags1")
# for word, pnt in test.items():
#     doc_ref = colection.document(word)
#     doc_ref.set({
#         "word": word,
#         "pnt": pnt,
#         "used": 0,
#         "updated_at": datetime.utcnow(),
#     })

# colection = db.collection("tags2")
# for word, pnt in KEIDOU.items():
#     doc_ref = colection.document(word)
#     doc_ref.set({
#         "word": word,
#         "pnt": pnt,
#         "used": 0,
#         "updated_at": datetime.utcnow(),
#     })

# colection = db.collection(u'system/TAG/TAG1')
# docs = colection.order_by("updated_at", direction=firestore.Query.ASCENDING).stream()
# data = []
# tmp = {}
# for doc in docs:
#     tmp = doc.to_dict()
#     del tmp["updated_at"], tmp["used"]
#     data.append(tmp)

# print(data)

# doc_ref = db.collection("system").document("TAG").collection("TAG1")
# doc_ref.set({
#     "形容動詞": KEIDOU,
#     # "形容詞", firestore.ArrayUnion(test),
# }, merge=True)

# for word, pnt in test:
#     system_service.add_tag(word,pnt)

kanjo = (
    ("つらい",-3),
    ("苦しい",-4),
    ("悲しい",-2),
    ("うれしい",4),
    ("楽しい",4),
)

aji = (
    ("甘い",-5),
    ("からい",-5),
    ("苦い",-5),
    ("しょっぱい",-5),
    ("すっぱい",-5),
    ("",-5),
    ("",-5),
    ("",-5),
    ("",-5),
    ("",-5),
)



# NEGATIVE_WORD_LIST = [
#     "死",
#     "ﾀﾋ",
#     "タヒ",
#     "しね",
#     "シネ",
#     "他界",
#     "亡く",
#     "成仏",
#     "逝去",
#     "老衰",
#     "絶命",
#     "不幸",
#     "先立",
#     "訃報"
#     "冥福"
#     "遺体"
#     "葬",
#     "殺",
#     "ころす",
#     "コロす",
#     "命の火",
#     "息の根",
#     "息を引",
#     "がん",
#     "末期",
#     "病",
#     "犯",
#     "罪",
#     "薬",
#     "違法",
#     "違反",
#     "逮捕",
#     "鬱",
#     "うつ",
#     "苦",
#     "暴",
#     "殴",
#     "痛",
#     "絶望",
#     "嫌い",
#     "きらい",
#     "キライ",
#     "うざい",
#     "ウザイ",
#     "消え",
#     "ばか",
#     "バカ",
#     "馬鹿",
#     "あほ",
#     "アホ",
#     "でぶ",
#     "デブ",
#     "はげ",
#     "ハゲ",
#     "くず",
#     "クズ",
# ]


# doc_ref = db.collection("system").document("NG_LIST")
# doc_ref.set({
#     "negative": firestore.ArrayUnion(NEGATIVE_WORD_LIST)
# })

# services.system_instance.add_ng_list("ごみ")

# "好き",
# "嫌い",
# for name in test:
#     tag_service.create(name)

# import os
# import tweepy
# import random

# from services.word import WordService


# auth = tweepy.OAuthHandler(
#     os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
# auth.set_access_token(os.environ['ACCESS_TOKEN'],
#                       os.environ['ACCESS_TOKEN_SECRET'])

# api = tweepy.API(auth)


# NEGATIVE_WORD_LIST = (
#     "死",
#     "ﾀﾋ",
#     "タヒ",
#     "他界",
#     "亡く",
#     "成仏",
#     "逝去",
#     "老衰",
#     "絶命",
#     "不幸",
#     "先立",
#     "訃報"
#     "冥福"
#     "遺体"
#     "葬",
#     "殺",
#     "命の火",
#     "息の根",
#     "息を引",
#     "がん",
#     "末期",
#     "病",
#     "犯",
#     "罪",
#     "薬",
#     "違法",
#     "違反",
#     "逮捕",
#     "鬱",
#     "うつ",
#     "苦",
#     "暴",
#     "殴",
#     "痛",
#     "絶望",
# )

# # api.update_status("投稿テスト")

# # public_tweets = api.home_timeline()
# # for tweet in public_tweets:
# #     print('-------------------------')
# #     print(tweet.text)


# # public_tweets = api.home_timeline()
# # for tweet in public_tweets:
# #     print('-------------------------')
# #     print(tweet.text)


# # for tweet in tweepy.Cursor(api.search, q='むーちゃん').items(10):
# #     # print(tweet)
# #     print(tweet.text)

# # class MyTweet:
# #     __init__


# class TweetService:

#     def post_tweet(self, msg):
#         """ ツイートする
#         """
#         api.update_status(msg)

#     def trend_tweet(self):
#         """ ツイッタートレンドからランダムでピックアップしてツイートする
#         """
#         # 日本のWOEID
#         woeid = 23424856
#         # トレンド取得
#         trends = api.trends_place(woeid)[0]
#         # トレンドワードからランダムで取得
#         trend_word = random.choice(trends["trends"])["name"]

#         #
#         topic = "(仮)"
#         msg = "最近「{}」って言葉をよく耳にするよ！\nでも、むーちゃんは何の事かよく分かんない。\nだれか教えにきて欲しいな！\nhttps://torichan.app".format(
#             trend_word, topic)
#         # ツイートする
#         self.post_tweet(msg)

#     def ng_word_check(self, word, limit):
#         """ 指定したワードが不適切な単語かチェックする
#             wordで検索したツイート20件の中にNGワードが一定数含まれているかチェック
#             limitで指定した数ヒットしたらTrueを返す
#         """
#         ng_word_hit = 0
#         for tweet in tweepy.Cursor(api.search, q=word, result_type="popular").items(20):
#             for ng_word in NEGATIVE_WORD_LIST:
#                 if ng_word in tweet.text:
#                     ng_word_hit = ng_word_hit + 1
#                     break
            
#             if ng_word_hit >= limit:
#                 return True

#         return False

#     def remembered_tweet(self, word):
#         """ 覚えたワードについてツイートする
#         """

#     def known_word_tweet(self):
#         """ 知っているワードについてツイートする
#         """

#     def unknown_word_tweet(self):
#         """ 意味を知らないワードについてツイートする
#         """


# tweet_saervice = TweetService()
# # tweet_saervice.trend_tweet()
# print( tweet_saervice.ng_word_check("喧嘩", 3) )




# from fastapi import APIRouter, HTTPException, Header, Request
# @router.get("/word_session", tags=["word"])
# def get_session(request: Request, session_id: Optional[str] = Header(None)):
#     """ セッションID取得
#         ヘッダーのsession_idパラメータに値が入っていない場合は新規idを発行
#     """
#     print(request.headers)
#     print(session_id)
#     return {"session_id": word_service.get_session(session_id)}