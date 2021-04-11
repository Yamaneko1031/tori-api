from uuid import UUID
from datetime import datetime

from google.cloud import firestore

db = firestore.Client()


class SystemService:
    collection_name = "system"

    def add_system_cnt(self, key):
        doc_ref = db.collection(self.collection_name).document("TOTAL")
        doc_ref.set({
            key: firestore.Increment(1),
        }, merge=True)
        doc_ref = db.collection(
            self.collection_name).document(datetime.today().strftime("%y-%m-%d"))
        doc_ref.set({
            key: firestore.Increment(1),
        }, merge=True)

    def get_system_data(self):
        doc = db.collection(
            self.collection_name).document("TOTAL").get()
        if not doc.exists:
            return
        return doc.to_dict()

    def add_session(self):
        doc_ref = db.collection(
            self.collection_name).document("TOTAL")
        doc_ref.set({
            "session_cnt": firestore.Increment(1)
        }, merge=True)

    def add_tag(self):
        doc_ref = db.collection(
            self.collection_name).document("TOTAL")
        doc_ref.set({
            "tag_cnt": firestore.Increment(1)
        }, merge=True)

    def add_word_create(self, word: str):
        doc_ref = db.collection(
            self.collection_name).document("TOTAL")
        doc_ref.set({
            "word_cnt": firestore.Increment(1)
        }, merge=True)

        doc_ref = db.collection(
            self.collection_name).document(datetime.today().strftime("%y-%m-%d"))
        doc_ref.set({
            "word_cnt": firestore.Increment(1),
            "word_create_list": firestore.ArrayUnion([word]),
        }, merge=True)

    def add_word_update(self, word: str):
        doc_ref = db.collection(
            self.collection_name).document("TOTAL")
        doc_ref.set({
            "word_update": firestore.Increment(1)
        }, merge=True)

        doc_ref = db.collection(
            self.collection_name).document(datetime.date)
        doc_ref.set({
            "word_update": firestore.Increment(1),
            "word_update_list": firestore.ArrayUnion([word]),
        }, merge=True)

    def add_unknown(self, word: str):
        doc_ref = db.collection(
            self.collection_name).document("TOTAL")
        doc_ref.set({
            "unknown_cnt": firestore.Increment(1)
        }, merge=True)

        doc_ref = db.collection(
            self.collection_name).document(datetime.today().strftime("%y-%m-%d"))
        doc_ref.set({
            "unknown_add_cnt": firestore.Increment(1),
            "unknown_add_list": firestore.ArrayUnion([word]),
        }, merge=True)

    def dec_unknown(self):
        doc_ref = db.collection(
            self.collection_name).document("TOTAL")
        doc_ref.set({
            "unknown_cnt": firestore.Increment(-1)
        }, merge=True)

        doc_ref = db.collection(
            self.collection_name).document(datetime.today().strftime("%y-%m-%d"))
        doc_ref.set({
            "unknown_dec_cnt": firestore.Increment(1),
        }, merge=True)

    def add_ng_list(self, word):
        doc_ref = db.collection(self.collection_name).document("NG_LIST")
        doc_ref.set({
            "negative": firestore.ArrayUnion([word])
        }, merge=True)

    def get_ng_list(self):
        doc = db.collection(self.collection_name).document("NG_LIST").get()
        return doc.to_dict()["negative"]

system_instance = SystemService()
