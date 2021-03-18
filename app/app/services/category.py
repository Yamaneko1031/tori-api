# from datetime import datetime

# from google.cloud import firestore

# from app import models

# db = firestore.Client()


# class WordService:
#     collection_name = "categories"

#     def create(self, word_create: models.WordCreate) -> models.WordAll:
#         data = models.WordAll(**word_create.dict()).dict()
#         doc_ref = db.collection(
#             self.collection_name).document(word_create.word)
#         doc_ref.set(data)
#         return self.get(word_create.word)

#     def get(self, word: str) -> models.WordAll:
#         doc_ref = db.collection(self.collection_name).document(word)
#         doc = doc_ref.get()
#         if doc.exists:
#             return models.WordAll(**doc.to_dict())
#         return

#     def update(self, word_update: models.WordUpdate) -> models.WordAll:
#         doc_ref = db.collection(
#             self.collection_name).document(word_update.word)

#         # パラメータを基に更新データ生成
#         data = {}
#         if word_update.mean != "":
#             data["mean"] = word_update.mean
#         if word_update.raiting > 0:
#             data["good"] = firestore.Increment(word_update.raiting)
#         elif word_update.raiting < 0:
#             data["bad"] = firestore.Increment(-word_update.raiting)
#         data["tag_list"] = firestore.ArrayUnion(word_update.tag_list)
#         data["updated_at"] = datetime.utcnow()

#         doc_ref.update(data)
#         doc = doc_ref.get()
#         if doc.exists:
#             return models.WordAll(**doc.to_dict())
#         return

#     # def delete(self, id: UUID) -> None:
#     #     db.collection(self.collection_name).document(str(id)).delete()