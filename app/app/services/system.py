from uuid import UUID
from datetime import datetime

from google.cloud import firestore

db = firestore.Client()


class SystemService:
    collection_name = "system"
    collection_session = "sessions"

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
        self.add_system_cnt("session_cnt")

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

    def get_ng_regex(self):
        doc = db.collection(self.collection_name).document("NG_LIST").get()
        return doc.to_dict()["regex"]

    def add_ng_ip(self, ip):
        doc_ref = db.collection(self.collection_name).document("NG_LIST")
        doc_ref.set({
            "ip": firestore.ArrayUnion([ip])
        }, merge=True)
        
    def get_ng_ip(self):
        doc = db.collection(self.collection_name).document("NG_LIST").get()
        return doc.to_dict()["ip"]
    
    def add_ng_session(self, session_id):
        doc_ref = db.collection(self.collection_name).document("NG_LIST")
        doc_ref.set({
            "session_id": firestore.ArrayUnion([session_id])
        }, merge=True)
        
    def get_ng_session(self):
        doc = db.collection(self.collection_name).document("NG_LIST").get()
        return doc.to_dict()["session_id"]
    
    def add_janken_result(self, result, session_id):
        if result == 0:
            set_result = "win_cnt"
        elif result == 1:
            set_result = "lose_cnt"
        elif result == 2:
            set_result = "draw_cnt"
        else:
            return False

        doc_ref = db.collection(self.collection_session).document(
            document_id=session_id)
        doc_ref.set({
            set_result: firestore.Increment(1)
        }, merge=True)

        doc_ref = db.collection(
            self.collection_name).document("TOTAL")
        doc_ref.set({
            set_result: firestore.Increment(1)
        }, merge=True)

        doc_ref = db.collection(
            self.collection_name).document(datetime.today().strftime("%y-%m-%d"))
        doc_ref.set({
            set_result: firestore.Increment(1)
        }, merge=True)
        return True
    
    def get_janken_result_total(self):
        ret = {
            "win_cnt": 0,
            "lose_cnt": 0,
            "draw_cnt": 0,
        }
        doc = db.collection(
            self.collection_name).document("TOTAL").get()
        if doc.exists:
            for key in ret.keys():
                if key in doc.to_dict():
                    ret[key] = doc.to_dict()[key]
                else:
                    ret[key] = 0
        return ret

    def get_janken_result_today(self):
        ret = {
            "win_cnt": 0,
            "lose_cnt": 0,
            "draw_cnt": 0,
        }
        doc = db.collection(
            self.collection_name).document(datetime.today().strftime("%y-%m-%d")).get()
        if doc.exists:
            for key in ret.keys():
                if key in doc.to_dict():
                    ret[key] = doc.to_dict()[key]
                else:
                    ret[key] = 0
        return ret

    def get_janken_result_session(self, session_id):
        ret = {
            "win_cnt": 0,
            "lose_cnt": 0,
            "draw_cnt": 0,
        }
        doc = db.collection(
            self.collection_session).document(document_id=session_id).get()
        if doc.exists:
            for key in ret.keys():
                if key in doc.to_dict():
                    ret[key] = doc.to_dict()[key]
        return ret

    def get_tweet_cnt(self):
        doc_ref = db.collection(
            self.collection_name).document("TOTAL")
        data = doc_ref.get().to_dict()
        if "tweet_cnt" in data:
            return data["tweet_cnt"]
        return 0

    def add_tweet_cnt(self):
        doc_ref = db.collection(
            self.collection_name).document("TOTAL")
        doc_ref.set({
            "tweet_cnt": firestore.Increment(1)
        }, merge=True)

    def reset_tweet_cnt(self):
        doc_ref = db.collection(
            self.collection_name).document("TOTAL")
        doc_ref.set({
            "tweet_cnt": 0
        }, merge=True)

system_instance = SystemService()
