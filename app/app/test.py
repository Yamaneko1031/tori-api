# import random
# from util import morpheme
# from google.cloud import firestore
# import time

# db = firestore.Client()

# text = "イヤホンとゲームとか映画やアニメになっている鬼滅の刃は東京の西の方にある地域。パソコンは高速に計算をすることが出来る機械"


# import MeCab

# tagger = MeCab.Tagger(
#     '-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
# text = "時間を知ることが出来るアイテム"

# print(tagger.parse(text))


# text = "a"

# 自動生成
# new_city_ref = db.collection(u'cities').document()
# new_city_ref.set({
#     "data1": "テスト",
#     "data2": 2,
# })

# phraseList = morpheme.disassemble(text)
# docs = db.collection(u'words').stream()
# get_data = docs.to_dict()

# phraseList2 = []
# for phrase in phraseList:
#     phraseList2.append(phrase["word"])

# print("{}:False".format(doc.id))


# unknown_ref = db.collection("unknowns").document()
# unknown_ref.set({
#     "word": "test1",
#     "kind": "test2",
#     "word_ref": 0,
#     "Interest": 1
# })
# docs = db.collection(u'unknowns').where(u'word', u'==', "いろはす").get()
# docs = db.collection(u'words').where(u'word', u'==', "いろはす").get()
# print(len(docs))
# for doc in docs:
#     print(doc.to_dict())


# def test4(text):
#     phraseList = morpheme.disassemble(text)
#     for key, value in phraseList.items():
#         doc = db.collection(u'words').document(key).get()
#         if not doc.exists:
#             doc = db.collection(u'unknowns').document(key).get()
#             if doc.exists:
#                 unknown_ref = db.collection("unknowns").document(key)
#                 unknown_ref.update({
#                     "word_ref": 0,
#                     "Interest": firestore.Increment(1)
#                 })
#             else:
#                 unknown_ref = db.collection("unknowns").document(key)
#                 unknown_ref.set({
#                     "word": key,
#                     "kind": value,
#                     "word_ref": 0,
#                     "Interest": 1
#                 })


# def test3(text):
#     phraseList = morpheme.disassemble(text)
#     for key, value in phraseList.items():
#         docs = db.collection(u'words').where(u'word', u'==', key).get()
#         if len(docs) == 0:
#             docs = db.collection(u'unknowns').where(u'word', u'==', key).get()
#             if len(docs) == 0:
#                 unknown_ref = db.collection("unknowns").document(key)
#                 unknown_ref.set({
#                     "word": key,
#                     "kind": value,
#                     "word_ref": 0,
#                     "Interest": 1
#                 })
#             elif len(docs) == 1:
#                 unknown_ref = db.collection("unknowns").document(key)
#                 unknown_ref.update({
#                     "word_ref": 0,
#                     "Interest": firestore.Increment(1)
#                 })


# def test2(word, mean):
#     word_ref = db.collection("words").document(word)
#     existList = []
#     phraseList = morpheme.disassemble(mean)
#     docs = db.collection(u'words').stream()
#     for doc in docs:
#         if doc.id in phraseList:
#             existList.append(doc.id)

#     knownList = []
#     unknownList = []
#     for key, value in phraseList.items():
#         if key in existList:
#             knownList.append({"word": key, "kind": value})
#         else:
#             unknownList.append({"word": key, "kind": value})
#             unknown_ref = db.collection("unknowns").document(key)
#             unknown_ref.set({
#                 "word": key,
#                 "kind": value,
#                 "word_ref": word_ref,
#                 "Interest": firestore.Increment(1)
#             }, merge=True)

#     retData = {}
#     if knownList:
#         retData["known"] = random.choice(knownList)
#     else:
#         retData["known"] = 0
#     if unknownList:
#         retData["unknown"] = random.choice(unknownList)
#     else:
#         retData["unknown"] = 0

#     return retData


# def test(text):
#     phraseList = morpheme.disassemble(text)
#     for phrase in phraseList:
#         # word_ref = db.collection("words").document(phrase["word"])
#         # doc = word_ref.get()
#         # query = db.collection(u'cities').where(u'capital', u'==', True)
#         # docs = db.collection(u'cities').where(u'capital', u'==', True).stream()

#         doc = db.collection("words").where(
#             u'word', u'==', phrase["word"]).stream()
#         # doc = word_ref.get()

#         if doc.exists:
#             phrase["know"] = True
#         else:
#             phrase["know"] = False
#             unknown_ref = db.collection("unknowns").document(phrase["word"])
#             doc = unknown_ref.get()
#             if doc.exists:
#                 unknown_ref.update({
#                     "word_ref": 0,
#                     "Interest": firestore.Increment(1)
#                 })
#             else:
#                 unknown_ref.set({
#                     "word": phrase["word"],
#                     "kind": phrase["kind"],
#                     "word_ref": 0,
#                     "Interest": 1
#                 })


# start = time.time()

# dic = test2("いろはす",text)

# elapsed_time = time.time() - start
# print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
# print(dic)

# print(phraseList)


# import MeCab

# tagger = MeCab.Tagger(
#     '-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
# text = "ゲームとか映画やアニメになっている鬼滅の刃は東京の西の方にある地域。高速に計算をすることが出来る機械"

# def analysis(word):
#     node = tagger.parseToNode(word)
#     result = tagger.parse(word)
#     phraseCnt = 0
#     result = {}
#     kind = ""
#     phraseList = []

#     while node:
#         if node.surface != "":  # ヘッダとフッタを除外
#             phraseCnt += 1
#             part = node.feature.split(",")
#             kind = ""

#             if (part[0] == "名詞"):
#                 if(part[1] == "一般"):
#                     kind = "名詞：一般"
#                 elif(part[1] == "サ変接続"):
#                     kind = "名詞：サ変接続"
#                 elif(part[1] == "固有名詞"):
#                     if(part[2] == "一般"):
#                         kind = "名詞：一般"
#                     elif(part[2] == "人名"):
#                         kind = "名詞：人名"
#                     elif(part[2] == "地域"):
#                         if(part[3] == "国"):
#                             kind = "名詞：国"
#                         elif(part[3] == "組織"):
#                             kind = "名詞：一般"
#                         else:
#                             kind = "名詞：地域"

#             elif (part[0] == "形容詞"):
#                 if(part[1] == "自立"):
#                     kind = "形容詞"

#             if(kind != ""):
#                 phraseList.append({"word": node.surface, "kind": kind})

#         node = node.next

#     if(phraseCnt > 1):
#         kind = "不明"

#     return phraseList


# result = analysis(text)
# print(result)


# node = tagger.parseToNode(text)
# partCnt = 0
# while node:
#     if node.surface != "":  # ヘッダとフッタを除外
#         partCnt += 1
#         part = node.feature.split(",")

#         if (part[0] == "名詞"):
#             if(part[1] == "固有名詞"):
#                 if(part[2] == "一般"):
#                 elif(part[2] == "人名"):
#                 elif(part[2] == "地域"):
#                     elif(part[3] == "国"):
#                     elif(part[3] == "一般"):
#                     elif(part[3] == "組織"):

#             if(part[1] == "一般"):


#         if (part[0] == "形容詞"):
#             if(part[1] == "自立"):


#         if (part[0] == "名詞"):
#             if(part[1] == "一般" or part[1] == "固有名詞"):
#                 print("{}って何？".format(node.surface))
#             elif(part[1] == "サ変接続"):
#                 print("僕も{}できるよ！！".format(node.surface))
#                 print("むーちゃんは{}苦手かもしれないなー".format(node.surface))
#         elif (part[0] == "形容詞"):
#             print(node.surface)

#     node = node.next

# print("単語数:{}".format(partCnt))

# while node:
#     if node.surface != "":  # ヘッダとフッタを除外
#         part = node.feature.split(",")
#         if (part[0] == "名詞"):
#             if(part[1] == "一般" or part[1] == "固有名詞"):
#                 print(node.surface)
#         elif (part[0] == "形容詞"):
#             print(node.surface)

#     node = node.next

# -Oyomi (ヨミ付与)
# -Ochasen (ChaSen互換)
# -Odump (全情報を出力)

# import os
# import tweepy

# auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
# auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])

# api = tweepy.API(auth)

# api.update_status("投稿テスト")

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print('-------------------------')
#     print(tweet.text)
