from google.cloud import firestore
from datetime import datetime
import time
import re
from pykakasi import kakasi

import sys

sys.path.append('/app')

import services
import models

import jaconv
from util import morpheme

db = firestore.Client()

kakasi = kakasi()
kakasi.setMode("J", "H")
conv = kakasi.getConverter()

system_service = services.system_instance
word_service = services.word_instance
tag_service = services.tag_instance

# data = {}
# data = morpheme.disassemble("幸せでガタガタで美しくて素敵なひと")

# for key, value in data.items():
#     if value == "形容詞" or value == "形容動詞":
#         kana = conv.do(key)
#         print("{}:{}".format(key,kana))


# word_create = models.WordCreate(word="パソコン",mean="高速に計算が出来て便利な機械。寂しい。")
# ret = word_service.create(word_create,"aaaaaa")


# tag_service.create_tag()

# data = []
# docs = db.collection("words").stream()
# for doc in docs:
#     data.append(doc.to_dict()["word"])

# print(data)


# if 2 <= len(data):
#     print( data )

# data = word_service.get_common_tag_word("空","大きい")
# print( data )

# word_service.add_tag_for_text("空","青くて大きくて自由で幸せなところ")

# system_service.add_janken_win(0)
# system_service.add_janken_lose(1)
# system_service.add_janken_draw(2)

# start = time.time()

# data = tag_service.get_random_choices()
# print( data )

# elapsed_time = time.time() - start
# print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

# word_create = models.WordCreate(word="雷",mean="空で発生する電気。怖ろしくて強くてあかるい。")
# ret = word_service.create(word_create,"aaaaaa")
# word_create = models.WordCreate(word="鳥",mean="空を飛ぶ生き物。強くてかっこいい。")
# ret = word_service.create(word_create,"aaaaaa")
# word_service.add_tag(word="雷", tag="不味い")
# word_service.add_tag(word="雷", tag="恐い")
# word_service.add_tag(word="雷", tag="怖ろしい")
# word_service.add_tag(word="鳥", tag="強い")
# word_service.add_tag(word="鳥", tag="強い")
# word_service.add_tag(word="鳥", tag="かわいい")
# word_service.add_tag(word="鳥", tag="格好いい")

# word_create = models.WordCreate(word="空",mean="上の方")
# ret = word_service.create(word_create,"aaaaaa")
# word_service.add_tag(word="空", tag="おおきい")

# tag_service.use_tag(word="雷", tag="温かい")

# word = "ab"
# re_roman = re.compile(r'^[a-zA-Z]+$') #a-z:小文字、A-Z:大文字
# status_kata = re_roman.fullmatch(word)
# print(status_kata)

# word = "木"
# re_hiragana = re.compile(r'[あ-ん]|[ア-ン]')
# status_hira = re_hiragana.fullmatch(word)
# print(status_hira)

# docs = db.collection_group("tags").where(u"test", u"==", 1).stream()
# for doc in docs:
#     print( doc.to_dict() )

# museums = db.collection_group(u'landmarks')\
#     .where(u'type', u'==', u'museum')
# docs = museums.stream()
# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')



# def collection_group_query(db):
#     # [START fs_collection_group_query_data_setup]
#     # [START firestore_query_collection_group_dataset]
#     cities = db.collection(u'cities')

    # sf_landmarks = cities.document(u'SF').collection(u'landmarks')
    # sf_landmarks.document().set({
    #     u'name': u'Golden Gate Bridge',
    #     u'type': u'bridge'
    # })
    # sf_landmarks.document().set({
    #     u'name': u'Legion of Honor',
    #     u'type': u'museum'
    # })
    # la_landmarks = cities.document(u'LA').collection(u'landmarks')
    # la_landmarks.document().set({
    #     u'name': u'Griffith Park',
    #     u'type': u'park'
    # })
    # la_landmarks.document().set({
    #     u'name': u'The Getty',
    #     u'type': u'museum'
    # })
    # dc_landmarks = cities.document(u'DC').collection(u'landmarks')
    # dc_landmarks.document().set({
    #     u'name': u'Lincoln Memorial',
    #     u'type': u'memorial'
    # })
    # dc_landmarks.document().set({
    #     u'name': u'National Air and Space Museum',
    #     u'type': u'museum'
    # })
    # tok_landmarks = cities.document(u'TOK').collection(u'landmarks')
    # tok_landmarks.document().set({
    #     u'name': u'Ueno Park',
    #     u'type': u'park'
    # })
    # tok_landmarks.document().set({
    #     u'name': u'National Museum of Nature and Science',
    #     u'type': u'museum'
    # })
    # bj_landmarks = cities.document(u'BJ').collection(u'landmarks')
    # bj_landmarks.document().set({
    #     u'name': u'Jingshan Park',
    #     u'type': u'park'
    # })
    # bj_landmarks.document().set({
    #     u'name': u'Beijing Ancient Observatory',
    #     u'type': u'museum'
    # })
    # [END firestore_query_collection_group_dataset]
    # [END fs_collection_group_query_data_setup]

    # [START fs_collection_group_query]
    # [START firestore_query_collection_group_filter_eq]
#     museums = db.collection_group(u'landmarks')\
#         .where(u'type', u'==', u'museum')
#     docs = museums.stream()
#     for doc in docs:
#         print(f'{doc.id} => {doc.to_dict()}')
#     # [END firestore_query_collection_group_filter_eq]
#     # [END fs_collection_group_query]
#     return docs

# collection_group_query(db)

# docs = db.collection("words").where("tags", "==", 1).stream()
# # docs = db.collection("words").where("tags", "in", ["強い"]).stream()
# for doc in docs:
#     print( doc )

# print( ret )

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
# test = {
#     "美味しい":5,
#     "明るい":2,
#     "暗い":-1,
#     "新しい":1,
#     "古い":-1,
#     "温かい":2,
#     "冷たい":0,
#     "暖かい":2,
#     "涼しい":1,
#     "暑い":-1,
#     "寒い":-1,
#     "熱い":-1,
#     "厚い":0,
#     "薄い":0,
#     "美しい":3,
#     "醜い":-3,
#     "大きい":2,
#     "小さい":2,
#     "重い":0,
#     "軽い":0,
#     "硬い":0,
#     "柔らかい":2,
#     "厳しい":-2,
#     "優しい":2,
#     "高い":2,
#     "低い":0,
#     "安い":0,
#     "近い":0,
#     "遠い":0,
#     "強い":2,
#     "弱い":-1,
#     "長い":1,
#     "短い":-1,
#     "早い":0,
#     "遅い":0,
#     "速い":3,
#     "広い":2,
#     "狭い":-2,
#     "太い":0,
#     "細い":0,
#     "難しい":-3,
#     "易しい":2,
#     "良い":4,
#     "悪い":-4,
#     "不味い":-5,
#     "すごい":4,
#     "偉い":2,
# }

# KEIDOU = {
#     "便利":2,
#     "不便":-1,
#     "綺麗":3,
#     "上品":2,
#     "下品":-1,
#     "なめらか":1,
#     "のどか":1,
#     "幸せ":4,
#     "専門的":0,
#     "にぎやか":1,
#     "静か":1,
#     "ステキ":3,
#     "華やか":2,
#     "壮大":1,
#     "偉大":2,
#     "爽やか":1,
#     "有名":2,
#     "人気":3,
#     "特殊":0,
#     "変":-1,
#     "健康":1,
#     "不思議":0,
#     "危険":-2,
#     "ぶきみ":-2,
# }


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

# kanjo = (
#     ("つらい",-3),
#     ("苦しい",-4),
#     ("悲しい",-2),
#     ("うれしい",4),
#     ("楽しい",4),
# )

# aji = (
#     ("甘い",-5),
#     ("からい",-5),
#     ("苦い",-5),
#     ("しょっぱい",-5),
#     ("すっぱい",-5),
#     ("",-5),
#     ("",-5),
#     ("",-5),
#     ("",-5),
#     ("",-5),
# )


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


# kind = [
#     "食べ物",
#     "生き物",
#     "",
# ]


#     # ["不気味","ぶきみ"],
#     # ["壮大","そうだい"],
#     # ["健康","病気"],

# KEIDOU = {
#     "便利":"べんり",
#     "不便":"ふべん",
#     "綺麗":"きれい",
#     "上品":"じょうひん",
#     "下品":"げひん",
#     "なめらか":"なめらか",
#     "のどか":"のどか",
#     "幸せ":"しあわせ",
#     "不幸":"ふこう",
#     "一般的":"いっぱんてき",
#     "専門的":"せんもんてき",
#     "にぎやか":"にぎやか",
#     "静か":"しずか",
#     "素敵":"すてき",
#     "華やか":"はなやか",
#     "地味":"じみ",
#     "壮大":"そうだい",
#     "偉大":"いだい",
#     "卑小":"ひしょう",
#     "爽やか":"さわやか",
#     "有名":"ゆうめい",
#     "特別":"とくべつ",
#     "無名":"むめい",
#     "人気":"にんき",
#     "不評":"ふひょう",
#     "特殊":"とくしゅ",
#     "変":"へん",
#     "健康":"けんこう",
#     "不思議":"ふしぎ",
#     "安全":"あんぜん",
#     "危険":"きけん",
#     "不気味":"ぶきみ",
# }

#     # ["たかい","やすい"],
#     # ["すごい","しょぼい"],
#     # ["ふとい","ほそい"],

# data = [
#     ["美味しい","不味い"],
#     ["明るい","暗い"],
#     ["新しい","古い"],
#     ["温かい","冷たい"],
#     ["暖かい","涼しい"],
#     ["暑い","寒い"],
#     ["熱い","冷たい"],
#     ["厚い","薄い"],
#     ["美しい","醜い"],
#     ["大きい","小さい"],
#     ["重い","軽い"],
#     ["柔らかい","硬い"],
#     ["優しい","厳しい"],
#     ["高い","低い"],
#     ["高い","安い"],
#     ["近い","遠い"],
#     ["強い","弱い"],
#     ["長い","短い"],
#     ["早い","遅い"],
#     ["速い","遅い"],
#     ["広い","狭い"],
#     ["太い","細い"],
#     ["難しい","易しい"],
#     ["良い","悪い"],
#     ["凄い","しょぼい"],
#     ["偉い","大したことない"],
# ]


# data1 = [
#     ["美味しい","不味い"],
#     ["明るい","暗い"],
#     ["新しい","古い"],
#     ["温かい","冷たい"],
#     ["熱い","寒い"],
#     ["美しい","醜い"],
#     ["大きい","小さい"],
#     ["重い","軽い"],
#     ["軟らかい","固い"],
#     ["優しい","厳しい"],
#     ["高い","低い"],
#     ["強い","弱い"],
#     ["長い","短い"],
#     ["速い","遅い"],
#     ["広い","狭い"],
#     ["難しい","易しい"],
#     ["良い","悪い"],
#     ["偉い","大したことない"],
#     ["可愛い","格好いい"]
#     ["便利","不便"],
#     ["華やか","地味"],
#     ["上品","下品"],
#     ["幸せ","不幸"],
#     ["一般的","専門的","特別"],
#     ["静か","賑やか"],
#     ["素敵","微妙"],
#     ["偉大","卑小"],
#     ["爽やか","陰湿"],
#     ["変","不思議"],
#     ["安全","危険"],
# ]

# ["近い","遠い"],
# ["有名","無名"],
# ["とくしゅ",""],
# ["にんき",""],
# ["なめらか","ざらざら"],
# ["のどか",""],

# tag_act = {
#     "美味しい":{"pnt":5,"part":"形容詞","text":"おいしい"},
#     "不味い":{"pnt":-5,"part":"形容詞","text":"まずい"},
#     "明るい":{"pnt":2,"part":"形容詞","text":"明るい"},
#     "暗い":{"pnt":-1,"part":"形容詞","text":"暗い"},
#     "新しい":{"pnt":1,"part":"形容詞","text":"新しい"},
#     "古い":{"pnt":-1,"part":"形容詞","text":"古い"},
#     "温かい":{"pnt":2,"part":"形容詞","text":"温かい"},
#     "冷たい":{"pnt":0,"part":"形容詞","text":"冷たい"},
#     "涼しい":{"pnt":1,"part":"形容詞","text":"すずしい"},
#     "熱い":{"pnt":-1,"part":"形容詞","text":"あつい"},
#     "寒い":{"pnt":0,"part":"形容詞","text":"さむい"},
#     "暑い":{"pnt":1,"part":"形容詞","text":"あつい"},
#     "厚い":{"pnt":0,"part":"形容詞","text":"あつい"},
#     "薄い":{"pnt":0,"part":"形容詞","text":"うすい"},
#     "美しい":{"pnt":3,"part":"形容詞","text":"美しい"},
#     "醜い":{"pnt":-3,"part":"形容詞","text":"みにくい"},
#     "大きい":{"pnt":2,"part":"形容詞","text":"大きい"},
#     "小さい":{"pnt":2,"part":"形容詞","text":"小さい"},
#     "重い":{"pnt":0,"part":"形容詞","text":"重い"},
#     "軽い":{"pnt":0,"part":"形容詞","text":"軽い"},
#     "硬い":{"pnt":0,"part":"形容詞","text":"かたい"},
#     "固い":{"pnt":0,"part":"形容詞","text":"かたい"},
#     "堅い":{"pnt":0,"part":"形容詞","text":"かたい"},
#     "柔らかい":{"pnt":2,"part":"形容詞","text":"やわらかい"},
#     "軟らかい":{"pnt":2,"part":"形容詞","text":"やわらかい"},
#     "厳しい":{"pnt":-2,"part":"形容詞","text":"きびしい"},
#     "優しい":{"pnt":2,"part":"形容詞","text":"やさしい"},
#     "高い":{"pnt":2,"part":"形容詞","text":"高い"},
#     "低い":{"pnt":0,"part":"形容詞","text":"低い"},
#     "安い":{"pnt":0,"part":"形容詞","text":"安い"},
#     "近い":{"pnt":0,"part":"形容詞","text":"近い"},
#     "遠い":{"pnt":0,"part":"形容詞","text":"遠い"},
#     "強い":{"pnt":2,"part":"形容詞","text":"強い"},
#     "弱い":{"pnt":-1,"part":"形容詞","text":"弱い"},
#     "長い":{"pnt":1,"part":"形容詞","text":"長い"},
#     "短い":{"pnt":-1,"part":"形容詞","text":"短い"},
#     "早い":{"pnt":0,"part":"形容詞","text":"はやい"},
#     "遅い":{"pnt":0,"part":"形容詞","text":"おそい"},
#     "速い":{"pnt":3,"part":"形容詞","text":"はやい"},
#     "広い":{"pnt":2,"part":"形容詞","text":"ひろい"},
#     "狭い":{"pnt":-2,"part":"形容詞","text":"せまい"},
#     "太い":{"pnt":0,"part":"形容詞","text":"太い"},
#     "細い":{"pnt":0,"part":"形容詞","text":"細い"},
#     "難しい":{"pnt":-3,"part":"形容詞","text":"むずかしい"},
#     "易しい":{"pnt":2,"part":"形容詞","text":"やさしい"},
#     "良い":{"pnt":4,"part":"形容詞","text":"良い"},
#     "悪い":{"pnt":-4,"part":"形容詞","text":"わるい"},
#     "凄い":{"pnt":4,"part":"形容詞","text":"すごい"},
#     "偉い":{"pnt":2,"part":"形容詞","text":"えらい"},
#     "しょぼい":{"pnt":-3,"part":"形容詞","text":"しょぼい"},
#     "大したことない":{"pnt":-2,"part":"形容詞","text":"大したことない"},
#     "可愛い":{"pnt":3,"part":"形容詞","text":"かわいい"},
#     "可愛らしい":{"pnt":3,"part":"形容詞","text":"かわいい"},
#     "格好いい":{"pnt":3,"part":"形容詞","text":"かっこいい"},
#     "怖い":{"pnt":-4,"part":"形容詞","text":"こわい"},
#     "恐い":{"pnt":-4,"part":"形容詞","text":"こわい"},
#     "怖ろしい":{"pnt":-4,"part":"形容詞","text":"おそろしい"},
#     "恐ろしい":{"pnt":-4,"part":"形容詞","text":"おそろしい"},
#     "嬉しい":{"pnt":3,"part":"形容詞","text":"うれしい"},
#     "悲しい":{"pnt":-1,"part":"形容詞","text":"かなしい"},

#     "便利":{"pnt":3,"part":"形容動詞","text":"便利"},
#     "不便":{"pnt":-2,"part":"形容動詞","text":"不便"},
#     "綺麗":{"pnt":3,"part":"形容動詞","text":"きれい"},
#     "汚い":{"pnt":-3,"part":"形容詞","text":"きたない"},
#     "上品":{"pnt":1,"part":"形容動詞","text":"上品"},
#     "下品":{"pnt":-1,"part":"形容動詞","text":"下品"},
#     "滑らか":{"pnt":2,"part":"形容動詞","text":"なめらか"},
#     "長閑":{"pnt":2,"part":"形容動詞","text":"のどか"},
#     "幸せ":{"pnt":4,"part":"形容動詞","text":"しあわせ"},
#     "不幸":{"pnt":-2,"part":"形容動詞","text":"不幸"},
#     "一般的":{"pnt":1,"part":"形容動詞","text":"一般的"},
#     "専門的":{"pnt":1,"part":"形容動詞","text":"専門的"},
#     "賑やか":{"pnt":2,"part":"形容動詞","text":"にぎやか"},
#     "静か":{"pnt":1,"part":"形容動詞","text":"静か"},
#     "素敵":{"pnt":4,"part":"形容動詞","text":"すてき"},
#     "微妙":{"pnt":-2,"part":"形容動詞","text":"びみょう"},
#     "華やか":{"pnt":3,"part":"形容動詞","text":"華やか"},
#     "地味":{"pnt":1,"part":"形容動詞","text":"地味"},
#     "壮大":{"pnt":2,"part":"形容動詞","text":"壮大"},
#     "偉大":{"pnt":4,"part":"形容動詞","text":"偉大"},
#     "卑小":{"pnt":-2,"part":"形容動詞","text":"卑小"},
#     "爽やか":{"pnt":1,"part":"形容動詞","text":"さわやか"},
#     "陰湿":{"pnt":1,"part":"形容動詞","text":"いんしつ"},
#     "有名":{"pnt":3,"part":"形容動詞","text":"有名"},
#     "特別":{"pnt":4,"part":"形容動詞","text":"特別"},
#     "無名":{"pnt":0,"part":"形容動詞","text":"無名"},
#     "人気":{"pnt":2,"part":"形容動詞","text":"人気"},
#     "不評":{"pnt":-2,"part":"形容動詞","text":"不評"},
#     "特殊":{"pnt":1,"part":"形容動詞","text":"とくしゅ"},
#     "変":{"pnt":0,"part":"形容動詞","text":"変"},
#     "健康":{"pnt":1,"part":"形容動詞","text":"健康"},
#     "不思議":{"pnt":1,"part":"形容動詞","text":"ふしぎ"},
#     "安全":{"pnt":1,"part":"形容動詞","text":"安全"},
#     "危険":{"pnt":-2,"part":"形容動詞","text":"危険"},
#     "不気味":{"pnt":-2,"part":"形容動詞","text":"ぶきみ"},
#     "まとも":{"pnt":1,"part":"形容動詞","text":"まとも"},
# }

# colection = db.collection("act_tags")
# for key, value in tag_act.items():
#     # print(jaconv.hira2kata(key))
#     # print(key)
#     # print(value)
#     doc_ref = colection.document(key)
#     doc_ref.set(value)


# all_tag = {
#     # "美味しい": {"refer": "美味しい"},
#     # "不味い": {"refer": "不味い"},
#     # "明るい": {"refer": "明るい"},
#     # "暗い": {"refer": "暗い"},
#     # "新しい": {"refer": "新しい"},
#     # "古い": {"refer": "古い"},
#     # "温かい": {"refer": "温かい"},
#     # "冷たい": {"refer": "冷たい"},
#     # "涼しい": {"refer": "涼しい"},
#     # "熱い": {"refer": "熱い"},
#     # "寒い": {"refer": "寒い"},
#     # "暑い": {"refer": "暑い"},
#     # "厚い": {"refer": "厚い"},
#     # "薄い": {"refer": "薄い"},
#     # "美しい": {"refer": "美しい"},
#     # "醜い": {"refer": "醜い"},
#     # "大きい": {"refer": "大きい"},
#     # "小さい": {"refer": "小さい"},
#     # "重い": {"refer": "重い"},
#     # "軽い": {"refer": "軽い"},
#     # "硬い": {"refer": "硬い"},
#     # "固い": {"refer": "固い"},
#     # "堅い": {"refer": "堅い"},
#     # "柔らかい": {"refer": "柔らかい"},
#     # "軟らかい": {"refer": "軟らかい"},
#     # "厳しい": {"refer": "厳しい"},
#     # "優しい": {"refer": "優しい"},
#     # "高い": {"refer": "高い"},
#     # "低い": {"refer": "低い"},
#     # "安い": {"refer": "安い"},
#     # "近い": {"refer": "近い"},
#     # "遠い": {"refer": "遠い"},
#     # "強い": {"refer": "強い"},
#     # "弱い": {"refer": "弱い"},
#     # "長い": {"refer": "長い"},
#     # "短い": {"refer": "短い"},
#     # "早い": {"refer": "早い"},
#     # "遅い": {"refer": "遅い"},
#     # "速い": {"refer": "速い"},
#     # "広い": {"refer": "広い"},
#     # "狭い": {"refer": "狭い"},
#     # "太い": {"refer": "太い"},
#     # "細い": {"refer": "細い"},
#     # "難しい": {"refer": "難しい"},
#     # "易しい": {"refer": "易しい"},
#     # "良い": {"refer": "良い"},
#     # "悪い": {"refer": "悪い"},
#     # "凄い": {"refer": "凄い"},
#     # "偉い": {"refer": "偉い"},
#     # "しょぼい": {"refer": "しょぼい"},
#     # "大したことない": {"refer": "大したことない"},
#     # "可愛い": {"refer": "可愛い"},
#     # "可愛らしい": {"refer": "可愛らしい"},
#     # "格好いい": {"refer": "格好いい"},
#     # "怖い": {"refer": "怖い"},
#     # "恐い": {"refer": "恐い"},
#     # "怖ろしい": {"refer": "怖ろしい"},
#     # "恐ろしい": {"refer": "恐ろしい"},
#     # "嬉しい": {"refer": "嬉しい"},
#     # "悲しい": {"refer": "悲しい"},

#     # "便利": {"refer": "便利"},
#     # "不便": {"refer": "不便"},
#     # "綺麗": {"refer": "綺麗"},
#     # "汚い": {"refer": "汚い"},
#     # "上品": {"refer": "上品"},
#     # "下品": {"refer": "下品"},
#     # "滑らか": {"refer": "滑らか"},
#     # "長閑": {"refer": "長閑"},
#     # "幸せ": {"refer": "幸せ"},
#     # "不幸": {"refer": "不幸"},
#     # "一般的": {"refer": "一般的"},
#     # "専門的": {"refer": "専門的"},
#     # "賑やか": {"refer": "賑やか"},
#     # "静か": {"refer": "静か"},
#     # "素敵": {"refer": "素敵"},
#     # "微妙": {"refer": "微妙"},
#     # "華やか": {"refer": "華やか"},
#     # "地味": {"refer": "地味"},
#     # "壮大": {"refer": "壮大"},
#     # "偉大": {"refer": "偉大"},
#     # "卑小": {"refer": "卑小"},
#     # "爽やか": {"refer": "爽やか"},
#     # "陰湿": {"refer": "陰湿"},
#     # "有名": {"refer": "有名"},
#     # "特別": {"refer": "特別"},
#     # "無名": {"refer": "無名"},
#     # "人気": {"refer": "人気"},
#     # "不評": {"refer": "不評"},
#     # "特殊": {"refer": "特殊"},
#     # "変": {"refer": "変"},
#     # "健康": {"refer": "健康"},
#     # "不思議": {"refer": "不思議"},
#     # "安全": {"refer": "安全"},
#     # "危険": {"refer": "危険"},
#     # "不気味": {"refer": "不気味"},
#     # "まとも": {"refer": "まとも"},

#     # "おいしい": {"refer": "美味しい"},
#     # "あかるい": {"refer": "明るい"},
#     # "くらい": {"refer": "暗い"},
#     # "あたらしい": {"refer": "新しい"},
#     # "ふるい": {"refer": "古い"},
#     # "あたたかい": {"refer": "温かい"},
#     # "つめたい": {"refer": "冷たい"},
#     # "すずしい": {"refer": "涼しい"},
#     # "あつい": {"refer": "熱い"},
#     # "さむい": {"refer": "寒い"},
#     # "うすい": {"refer": "薄い"},
#     # "うつくしい": {"refer": "美しい"},
#     # "みにくい": {"refer": "醜い"},
#     # "おおきい": {"refer": "大きい"},
#     # "ちいさい": {"refer": "小さい"},
#     # "おもい": {"refer": "重い"},
#     # "かるい": {"refer": "軽い"},
#     # "かたい": {"refer": "固い"},
#     # "やわらかい": {"refer": "柔らかい"},
#     # "きびしい": {"refer": "厳しい"},
#     # "やさしい": {"refer": "優しい"},
#     # "たかい": {"refer": "高い"},
#     # "ひくい": {"refer": "低い"},
#     # "やすい": {"refer": "安い"},
#     # "ちかい": {"refer": "近い"},
#     # "とおい": {"refer": "遠い"},
#     # "つよい": {"refer": "強い"},
#     # "よわい": {"refer": "弱い"},
#     # "ながい": {"refer": "長い"},
#     # "みじかい": {"refer": "短い"},
#     # "はやい": {"refer": "速い"},
#     # "おそい": {"refer": "遅い"},
#     # "ひろい": {"refer": "広い"},
#     # "せまい": {"refer": "狭い"},
#     # "ふとい": {"refer": "太い"},
#     # "ほそい": {"refer": "細い"},
#     # "むずかしい": {"refer": "難しい"},
#     # "よい": {"refer": "良い"},
#     # "わるい": {"refer": "悪い"},
#     # "まずい": {"refer": "不味い"},
#     # "すごい": {"refer": "凄い"},
#     # "えらい": {"refer": "偉い"},
#     # "たいしたことない": {"refer": "大したことない"},
#     # "かわいい": {"refer": "可愛い"},
#     # "かっこいい": {"refer": "格好いい"},
#     # "べんり": {"refer": "便利"},
#     # "ふべん": {"refer": "不便"},
#     # "きれい": {"refer": "綺麗"},
#     # "じょうひん": {"refer": "上品"},
#     # "げひん": {"refer": "下品"},
#     # "なめらか": {"refer": "滑らか"},
#     # "のどか": {"refer": "長閑"},
#     # "しあわせ": {"refer": "幸せ"},
#     # "ふこう": {"refer": "不幸"},
#     # "いっぱんてき": {"refer": "一般的"},
#     # "せんもんてき": {"refer": "専門的"},
#     # "にぎやか": {"refer": "賑やか"},
#     # "しずか": {"refer": "静か"},
#     # "すてき": {"refer": "素敵"},
#     # "はなやか": {"refer": "華やか"},
#     # "じみ": {"refer": "地味"},
#     # "そうだい": {"refer": "壮大"},
#     # "いだい": {"refer": "偉大"},
#     # "ひしょう": {"refer": "卑小"},
#     # "さわやか": {"refer": "爽やか"},
#     # "ゆうめい": {"refer": "有名"},
#     # "とくべつ": {"refer": "特別"},
#     # "むめい": {"refer": "無名"},
#     # "にんき": {"refer": "人気"},
#     # "ふひょう": {"refer": "不評"},
#     # "とくしゅ": {"refer": "特殊"},
#     # "へん": {"refer": "変"},
#     # "けんこう": {"refer": "健康"},
#     # "ふしぎ": {"refer": "不思議"},
#     # "あんぜん": {"refer": "安全"},
#     # "きけん": {"refer": "危険"},
#     # "ぶきみ": {"refer": "不気味"},
#     "美味しくない": {"refer": "美味しくない"},
#     "おいしくない": {"refer": "美味しくない"},
# }

# colection = db.collection("act_tags")
# colection2 = db.collection("called_tags")
# for key, value in all_tag.items():
#     doc_ref = colection.document(value["refer"])
#     doc_ref2 = colection2.document(key)
#     doc_ref2.set({
#         "refer": doc_ref
#     })
# print(jaconv.hira2kata(key))
# print(key)
# print(value)
# doc_ref.set(value)




# colection = db.collection("act_tags")
# colection2 = db.collection("called_tags")

# data = colection2.document("あかるい").get().to_dict()["refer"].get().to_dict()
# print(data)

# data1 = [
#     ["美味しい", "不味い"],
#     ["明るい", "暗い"],
#     ["新しい", "古い"],
#     ["温かい", "冷たい"],
#     ["熱い", "寒い"],
#     ["美しい", "醜い"],
#     ["大きい", "小さい"],
#     ["重い", "軽い"],
#     ["軟らかい", "固い"],
#     ["優しい", "厳しい"],
#     ["高い", "低い"],
#     ["強い", "弱い"],
#     ["長い", "短い"],
#     ["速い", "遅い"],
#     ["広い", "狭い"],
#     ["難しい", "易しい"],
#     ["良い", "悪い"],
#     ["偉い", "大したことない"],
#     ["可愛い", "格好いい"],
#     ["便利", "不便"],
#     ["華やか", "地味"],
#     ["上品", "下品"],
#     ["幸せ", "不幸"],
#     ["一般的", "専門的", "特別"],
#     ["静か", "賑やか"],
#     ["素敵", "微妙"],
#     ["偉大", "卑小"],
#     ["爽やか", "陰湿"],
#     ["変", "不思議"],
#     ["安全", "危険"],
# ]

# import random

# data1 = []
# colection = db.collection("tag_choices")
# docs = colection.stream()
# for doc in docs:
#     data1.append(doc.to_dict()["list"])


# # print(random.choice(data1))

# ret = []
# # colection = db.collection("act_tags")
# colection2 = db.collection("called_tags")

# data2 = random.choice(data1)

# for key in data2:
#     print(key)
#     ret.append( colection2.document(key).get().to_dict()["refer"].get().to_dict() )


# tag_service = services.tag_instance

# # print( tag_service.get_random_coices() )

# data = tag_service.get_tag("明るイ")
# print( data )


# for data in data1:
#     colection.document().set({
#         "list": firestore.ArrayUnion(data)
#     })

#         docs = colection.order_by("updated_at", direction=firestore.Query.DESCENDING).stream()
#         data = []
#         for doc in docs:
#             tmp = doc.to_dict()
#             del tmp["updated_at"], tmp["used"]
#             data.append(tmp)


# test = {
#     "おいしい":"美味しい",
#     "あかるい":"明るい",
#     "くらい":"暗い",
#     "あたらしい":"新しい",
#     "ふるい":"古い",
#     "あたたかい":"温かい",
#     "つめたい":"冷たい",
#     "すずしい":"涼しい",
#     "あつい":"熱い",
#     "さむい":"寒い",
#     "うすい":"薄い",
#     "うつくしい":"美しい",
#     "みにくい":"醜い",
#     "おおきい":"大きい",
#     "ちいさい":"小さい",
#     "おもい":"重い",
#     "かるい":"軽い",
#     "かたい":"固い",
#     "やわらかい":"柔らかい",
#     "きびしい":"厳しい",
#     "やさしい":"優しい",
#     "たかい":"高い",
#     "ひくい":"低い",
#     "やすい":"安い",
#     "ちかい":"近い",
#     "とおい":"遠い",
#     "つよい":"強い",
#     "よわい":"弱い",
#     "ながい":"長い",
#     "みじかい":"短い",
#     "はやい":"速い",
#     "おそい":"遅い",
#     "ひろい":"広い",
#     "せまい":"狭い",
#     "ふとい":"太い",
#     "ほそい":"細い",
#     "むずかしい":"難しい",
#     "よい":"良い",
#     "わるい":"悪い",
#     "まずい":"不味い",
#     "すごい":"凄い",
#     "えらい":"偉い",
#     "たいしたことない":"大したことない",
#     "かわいい":"可愛い",
#     "かっこいい":"格好いい",
#     "べんり":"便利",
#     "ふべん":"不便",
#     "きれい":"綺麗",
#     "じょうひん":"上品",
#     "げひん":"下品",
#     "なめらか":"滑らか",
#     "のどか":"長閑",
#     "しあわせ":"幸せ",
#     "ふこう":"不幸",
#     "いっぱんてき":"一般的",
#     "せんもんてき":"専門的",
#     "にぎやか":"賑やか",
#     "しずか":"静か",
#     "すてき":"素敵",
#     "はなやか":"華やか",
#     "じみ":"地味",
#     "そうだい":"壮大",
#     "いだい":"偉大",
#     "ひしょう":"卑小",
#     "さわやか":"爽やか",
#     "ゆうめい":"有名",
#     "とくべつ":"特別",
#     "むめい":"無名",
#     "にんき":"人気",
#     "ふひょう":"不評",
#     "とくしゅ":"特殊",
#     "へん":"変",
#     "けんこう":"健康",
#     "ふしぎ":"不思議",
#     "あんぜん":"安全",
#     "きけん":"危険",
#     "ぶきみ":"不気味",
# }

# test = {
#     "美味しい":"おいしい",
#     "おいしい":5,
#     "明るい":"あかるい",
#     "あかるい":2,
#     "暗い":"くらい",
#     "くらい":-1,
#     "新しい":"あたらしい",
#     "あたらしい":1,
#     "古い":"ふるい",
#     "ふるい":-1,
#     "温かい":"あたたかい",
#     "あたたかい":2,
#     "冷たい":"つめたい",
#     "つめたい":0,
#     "暖かい":"あたたかい",
#     "あたたかい":2,
#     "涼しい":"すずしい",
#     "すずしい":1,
#     "暑い":"あつい",
#     "あつい":-1,
#     "寒い":"さむい",
#     "さむい":-1,
#     "熱い":"あつい",
#     "あつい":-1,
#     "厚い":"あつい",
#     "あつい":0,
#     "薄い":"うすい",
#     "うすい":0,
#     "美しい":"うつくしい",
#     "うつくしい":3,
#     "醜い":"みにくい",
#     "みにくい":-3,
#     "大きい":"おおきい",
#     "おおきい":2,
#     "小さい":"ちいさい",
#     "ちいさい":2,
#     "重い":"おもい",
#     "おもい":0,
#     "軽い":"かるい",
#     "かるい":0,
#     "硬い":"かたい",
#     "かたい":0,
#     "柔らかい":"やわらかい",
#     "やわらかい":2,
#     "厳しい":"きびしい",
#     "きびしい":-2,
#     "優しい":"やさしい",
#     "やさしい":2,
#     "高い":"たかい",
#     "たかい":2,
#     "低い":"ひくい",
#     "ひくい":0,
#     "安い":"やすい",
#     "やすい":0,
#     "近い":"ちかい",
#     "ちかい":0,
#     "遠い":"とおい",
#     "とおい":0,
#     "強い":"つよい",
#     "つよい":2,
#     "弱い":"よわい",
#     "よわい":-1,
#     "長い":"ながい",
#     "ながい":1,
#     "短い":"みじかい",
#     "みじかい":-1,
#     "早い":"はやい",
#     "はやい":0,
#     "遅い":"おそい",
#     "おそい":0,
#     "速い":"はやい",
#     "はやい":3,
#     "広い":"ひろい",
#     "ひろい":2,
#     "狭い":"せまい",
#     "せまい":-2,
#     "太い":"ふとい",
#     "ふとい":0,
#     "細い":"ほそい",
#     "ほそい":0,
#     "難しい":"むずかしい",
#     "むずかしい":-3,
#     "易しい":"やさしい",
#     "やさしい":2,
#     "良い":"よい",
#     "よい":4,
#     "悪い":"わるい",
#     "わるい":-4,
#     "不味い":"まずい",
#     "まずい":-5,
#     "凄い":"すごい",
#     "すごい":4,
#     "偉い":"えらい",
#     "えらい":2,
#     "しょぼい":-3,
#     "大したことない":"たいしたことない",
#     "たいしたことない":-2,
#     "可愛い":"かわいい",
#     "かわいい":3,
#     "格好いい":"かっこいい",
#     "かっこいい":3,

#     "べんり":3,
#     "便利":"べんり",
#     "ふべん":-2,
#     "不便":"ふべん",
#     "きれい":3,
#     "綺麗":"きれい",
#     "上品":"じょうひん",
#     "下品":"げひん",
#     "なめらか":"なめらか",
#     "のどか":"のどか",
#     "幸せ":"しあわせ",
#     "不幸":"ふこう",
#     "一般的":"いっぱんてき",
#     "専門的":"せんもんてき",
#     "にぎやか":"にぎやか",
#     "静か":"しずか",
#     "素敵":"すてき",
#     "華やか":"はなやか",
#     "地味":"じみ",
#     "壮大":"そうだい",
#     "偉大":"いだい",
#     "卑小":"ひしょう",
#     "爽やか":"さわやか",
#     "有名":"ゆうめい",
#     "特別":"とくべつ",
#     "無名":"むめい",
#     "人気":"にんき",
#     "不評":"ふひょう",
#     "特殊":"とくしゅ",
#     "変":"へん",
#     "健康":"けんこう",
#     "不思議":"ふしぎ",
#     "安全":"あんぜん",
#     "危険":"きけん",
#     "不気味":"ぶきみ",
# }

# for key, value in test.items():
#     print(jaconv.hira2kata(key))
