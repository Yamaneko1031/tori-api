# from google.cloud.firestore_v1 import Transaction
# from google.cloud import firestore
# import random
# import models
# from uuid import uuid4

# db = firestore.Client()

# docs = db.collection(u'words').where(u'tag_list', u'array_contains', u'便利').stream()
# docs = db.collection(u'words').where(u'tag_list', u'in', [[u'便利']]).stream()

# for doc in docs:
#     print(doc.to_dict()['word'])


# test_ref = db.collection("test").document("プリン")
# unknown_ref = db.collection("unknowns").document("卵")

# data1 = {
#     "word": "プリン",
#     "mean": "卵と牛乳に砂糖を入れて固めたもの",
#     "unknown_ref": unknown_ref,
# }

# data2 = {
#     "word": "卵",
#     "test_ref": test_ref,
# }
# test_ref.set(data1)
# unknown_ref.set(data2)

# cities_ref = db.collection("unknowns")
# query = cities_ref.order_by("name").limit_to_last(2)


# getDataList = []
# docs = db.collection(u'words').order_by(u'created_at', direction=firestore.Query.DESCENDING).limit(5).stream()
# for doc in docs:
#     word_dict = doc.to_dict()
#     getDataList.append({
#         "word": word_dict["word"],
#         "mean": word_dict["word"],
#         "tag_list": word_dict["tag_list"],
#     })

# ret = random.choice(getDataList)
# print( ret )

#     print( doc.to_dict() )
#     # print( doc.to_dict()["word_ref"] )
#     print( doc.to_dict()["word_ref"].get().to_dict() )
# for doc in docs:
#     print( doc.to_dict() )
#     # print( doc.to_dict()["word_ref"] )
#     print( doc.to_dict()["word_ref"].get().to_dict() )


# doc_ref = db.collection("unknowns").document("卵")
# doc = doc_ref.get()
# if doc.exists:
#     print(doc.to_dict()["test_ref"].get().to_dict())

# ref = db.collection("test").document("卵")
# docs = ref.get()
# for doc in docs:
#     print(doc.to_dict())
# print(doc)

# doc_ref = db.collection(self.collection_name).document(word)
# doc = doc_ref.get()
# if doc.exists:
#     return models.WordAll(**doc.to_dict())
# return


# -------------------------------------------------------
# トランザクション サンプル
# -------------------------------------------------------
# db = firestore.Client()
# sessions = db.collection('sessions')

# greetings = [
#     'Hello World',
#     'Hallo Welt',
#     'Ciao Mondo',
#     'Salut le Monde',
#     'Hola Mundo',
# ]


# session_id = "48cc0623-0aae-4991-b80a-30588699a882"

# @firestore.transactional
# def get_session_data(transaction, session_id):
#     """ Looks up (or creates) the session with the given session_id.
#         Creates a random session_id if none is provided. Increments
#         the number of views in this session. Updates are done in a
#         transaction to make sure no saved increments are overwritten.
#     """

#     # if session_id is None:
#     #     session_id = str(uuid4())   # Random, unique identifier

#     # doc_ref = sessions.document(document_id=session_id)
#     # doc = doc_ref.get(transaction=transaction)
#     # if doc.exists:
#     #     session = doc.to_dict()
#     # else:
#     #     session = {
#     #         'greeting': random.choice(greetings),
#     #         'views': 0
#     #     }

#     # session['views'] += 1   # This counts as a view
#     # transaction.set(doc_ref, session)

#     # session['session_id'] = session_id

#     # transaction = db.transaction()

#     taset_db = db.collection('taset_db1')
#     test_ref = taset_db.document("BlimUBXspmBsJcVcOLii")
#     doc = test_ref.get(transaction=transaction)
#     print(doc.to_dict())
#     data = {
#         "word": "クッキー",
#         "test_ref": test_ref,
#     }
#     transaction.set(test_ref, data)

#     print( test_ref.get().to_dict() )
#     print( test_ref.get(transaction=transaction).to_dict() )

#     taset_db = db.collection('taset_db2')
#     test_ref = taset_db.document("D4kzDPbagCIEWZNni3tR")
#     data = {
#         "word": "卵卵",
#         "test_ref": test_ref,
#     }
#     transaction.set(test_ref, data)


#     return 1


# def home():
#     transaction = db.transaction()
#     session = get_session_data(transaction, session_id)
#     print(session)
#     return session_id


# id = home()

# import logging
# logger = logging.getLogger()
# # formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
# logging.basicConfig(format="%(asctime)s:%(filename)s:%(lineno)d:%(process)d:%(thread)d:%(levelname)s:%(message)s")
# logger.error("session_idがdbに存在しない")
# logger.info("session_idがdbに存在しない")
# logger.debug("session_idがdbに存在しない")
# logger.warning("session_idがdbに存在しない")

# from uuid import UUID
# from uuid import uuid4

# print(uuid4())
# print(UUID())


# test_ref = db.collection("test").document("プリン")
# data1 = {
#     "word": "プリン",
#     "mean": "卵と牛乳に砂糖を入れて固めたもの",
#     "data": {
#         "a": 4,
#         "b": 10,
#     }
# }
# # test_ref.set(data1)
# db.collection("test").add(data1)


# getDataList = []
# # docs = db.collection(u'words').order_by(u'created_at', direction=firestore.Query.DESCENDING).limit(3).stream()

# # docs = db.collection(u'words').where(u'tag_list', u'array_contains', u'便利').stream()
# docs = db.collection(u'words').where("cnt", "==", 4).order_by(u'created_at', direction=firestore.Query.DESCENDING).limit(3).stream()
# for doc in docs:
#     word_dict = doc.to_dict()
#     getDataList.append({
#         "word": word_dict["word"],
#         "mean": word_dict["word"],
#         # "tag_list": word_dict["tag_list"],
#     })

# print( getDataList )


# from uuid import uuid4
# # import api
# # import services
# import models

# def create(word_create: models.WordCreate, taught: str):
#     # 新規単語の追加
#     data = models.WordAll(**word_create.dict()).dict()
#     data["taught"] = str(taught)
#     ret = db.collection("test").add(data)
#     return ret[1].get().to_dict()

# a = create(models.WordCreate(word = "目薬", mean = "目に入れる薬"),uuid4())

# print( a )

# word = "目薬"
# docs = db.collection("test").where("word", "==", word).limit(1).get()

# if docs:
#     print( docs[0].to_dict() )
# for doc in docs:

# docs = db.collection(u'words').where(u'tag_list', u'in', [[u'便利']]).stream()
# doc = docks[0].get()
# print( doc.to_dict() )


# getDataList = ["a","b"]
# docs = db.collection(self.collection_unknown).where("taught", "==", taught).limit(10).stream()
# for doc in docs:
#     unknown = doc.to_dict()
#     ref = doc.to_dict()["word_ref"].get().to_dict()

#     getDataList.append({
#         "word": unknown["word"],
#         "kind": unknown["kind"],
#         "ref": {
#             "word": ref["word"],
#             "mean": ref["mean"],
#         }
#     })

# if not getDataList:
#     getDataList = [{"error": "taught none"}]

# print( random.choice(getDataList) )


# unknownテーブルにある場合は削除する
# docs = db.collection("test").where("word", "==", "目薬").stream()
# for doc in docs:
#     doc._reference.delete()


# def create(word_create: models.WordCreate, taught: str):
#     """ 新規単語の追加
#     """

#     # unknownテーブルにある場合は削除する
#     docs = db.collection("unknowns").where("word", "==", word_create.word).stream()
#     for doc in docs:
#         doc._reference.delete()

#     data = models.WordAll(**word_create.dict()).dict()
#     data["taught"] = taught
#     addBuff = db.collection("words").add(data)

#     return models.WordAll(**addBuff[1].to_dict())

# a = create(models.WordCreate(word = "スープ", mean = "水気の多い食べ物"),str(uuid4()))

# print(a)


# def create(word_create: models.WordCreate, taught: str):
#     """ 新規単語の追加
#     """

#     # unknownテーブルにある場合は削除する
#     docs = db.collection("unknowns").where("word", "==", word_create.word).stream()
#     for doc in docs:
#         doc._reference.delete()

#     data = models.WordAll(**word_create.dict()).dict()
#     data["taught"] = taught
#     addBuff = db.collection("words").add(data)

#     return models.WordAll(**addBuff[1].to_dict())

# a = create(models.WordCreate(word = "スープ", mean = "水気の多い食べ物"),str(uuid4()))

# print(a)


# @firestore.transactional
# def create_tr(transaction: Transaction, word_create: models.WordCreate, taught: str):
#     """ 新規単語の追加で呼び出すトランザクション処理
#     """

#     # unknownsコレクションに追加にある場合は削除する
#     docs = db.collection("unknowns").where(
#         "word", "==", word_create.word).stream()
#     for doc in docs:
#         transaction.delete(doc._reference)

#     # wordsコレクションに追加
#     word_data = models.WordAll(**word_create.dict()).dict()
#     word_data["taught"] = taught
#     word_ref = db.collection("words").document()
#     transaction.set(word_ref, word_data)

#     # sessionsコレクション更新
#     session_ref = db.collection("sessions").document(document_id=taught)
#     session_data = {
#         "teachWords": firestore.ArrayUnion([word_create.word]),
#         "teachRefs": firestore.ArrayUnion([word_ref]),
#         "teachCnt": firestore.Increment(1),
#     }
#     transaction.set(session_ref, session_data, merge=True)

#     return word_data


# def create(word_create: models.WordCreate, taught: str):
#     """ 新規単語の追加
#     """
#     transaction = db.transaction()
#     ref = create_tr(transaction, word_create, taught)
#     return models.WordAll(**ref.get().to_dict())

# taught = "aaa437b8-5616-4840-9908-9fd46f93e653"

# a = create(models.WordCreate(word="おかき", mean="鶏のお肉"), str(uuid4()))
# a = create(models.WordCreate(word="枕", mean="寝るときに頭を乗せるやつ"), taught)

# print(a)


# taught = "aaa437b8-5616-4840-9908-9fd46f93e653"
# doc_dict = db.collection("sessions").document(document_id=taught).get().to_dict()
# for ref in doc_dict["teachWords"]:
#     data = ref.get().to_dict()
#     print("{}:{}".format(data["word"],data["mean"]))


# from util import morpheme

# class WordService:
#     collection_name = "words"
#     collection_unknown = "unknowns"
#     collection_session = "sessions"

#     def knownList(self, word: str, mean: str):
#         """ 知っている単語、知らない単語の中からランダムで一つ選んで返す
#         """
#         # 意味の中から認識可能な単語を取得
#         phraseList = morpheme.disassemble(mean)

#         # 知っている単語、知らない単語の一覧を作成
#         knownList = []
#         unknownList = []
#         for key, value in phraseList.items():
#             docs = db.collection(self.collection_name).where(
#                 "word", "==", key).limit(1).get()
#             if docs:
#                 knownList.append({"word": key, "kind": value})
#             else:
#                 unknownList.append({"word": key, "kind": value})
#                 unknown_ref = db.collection(
#                     self.collection_unknown).document(key)
#                 unknown_ref.set({
#                     "word": key,
#                     "kind": value,
#                     "word_ref": db.collection(self.collection_name).document(word),
#                     "Interest": firestore.Increment(1)
#                 }, merge=True)

#         # 知っている単語、知らない単語の中からランダムで一つ選んで返す
#         retData = {"known": 0, "unknown": 0}
#         if knownList:
#             retData["known"] = random.choice(knownList)
#         if unknownList:
#             retData["unknown"] = random.choice(unknownList)

#         return retData


# taught = "4f7a1725-cb78-470a-9f5d-254ed1c73204"
# get_data_list = []

# docs = db.collection('words').order_by('updated_at').stream()
# cnt = 0
# for doc in docs:
#     word_dict = doc.to_dict()
#     if "taught" in word_dict:
#         if word_dict["taught"] != taught:
#             cnt = cnt + 1
#             get_data_list.append({
#                 "word": word_dict["word"],
#                 # "mean": word_dict["word"],
#                 # "tag_list": word_dict["tag_list"],
#                 # "time": word_dict["updated_at"],
#             })
#     if cnt >= 20:
#         break

# # print(random.choice(get_data_list))
# print(get_data_list)


# from test3 import test3_func, Test3Class

# test3_func()
# ins = Test3Class("test_db")
# ins.test()


# from test4 import test4_func

# test4_func()