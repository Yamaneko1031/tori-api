import os
import random
import logging
from uuid import uuid4
from datetime import datetime
from typing import List

from google.cloud import firestore

from app.util import morpheme
from app import models, services

db = firestore.Client()
logger = logging.getLogger(__name__)


class UserLogService:
    collection_name = "action_log"
    sub_collection_teach = "teach_log"
    collection_word = "words"
    # sub_collection_mean_update = "mean_update_log"

    def __init__(self):
        """ コンストラクタ
        """
        return

    def add_teach_log(self, word: str, mean: str, ip_adress: str, session_id: str, create_ret):
        day_ref = db.collection(
            self.collection_name).document(datetime.today().strftime("%Y-%m-%d"))
        doc = day_ref.collection(self.sub_collection_teach).document()
        doc.set({
            "action": create_ret["action"],
            "word": word,
            "mean": mean,
            "pre_mean": create_ret["pre_mean"],
            "ip_address": ip_adress,
            "tweet_state": create_ret["tweet"]["state"],
            "tweet_id": create_ret["tweet"]["id"],
            "word_ref": create_ret["create_ref"],
            "session_id": session_id,
            "created_at": datetime.utcnow()
        })

        return doc.id

    def get_teach_logs(self, year: int, month: int, day: int):
        # print("{:04}-{:02}-{:02}".format(year, month, day))
        day_ref = db.collection(
            self.collection_name).document("{:04}-{:02}-{:02}".format(year, month, day))

        docs = day_ref.collection(self.sub_collection_teach).order_by(
            u'created_at', direction=firestore.Query.DESCENDING).stream()

        teach_list = []
        for doc in docs:
            data = doc.to_dict()
            data["created_at"] = data["created_at"].strftime(
                "%Y/%m/%d %H:%M:%S")
            data["id"] = doc.id
            if "word_ref" in data:
                word_doc = db.collection(self.collection_word).document(
                    data["word_ref"]).get()
                if word_doc:
                    word_data = word_doc.to_dict()
                    data["now_mean"] = word_data["mean"]
                else:
                    data["now_mean"] = ""

            teach_list.append(data)

        return teach_list

    def get_teach_log(self, year: int, month: int, day: int, id: str):
        # print("{:04}-{:02}-{:02}".format(year, month, day))
        day_ref = db.collection(
            self.collection_name).document("{:04}-{:02}-{:02}".format(year, month, day))

        return day_ref.collection(self.sub_collection_teach).document(id).get().to_dict()

    def update_teach_log_tweet_delete(self, year: int, month: int, day: int, id: str):
        # print("{:04}-{:02}-{:02}".format(year, month, day))
        day_ref = db.collection(
            self.collection_name).document("{:04}-{:02}-{:02}".format(year, month, day))

        day_ref.collection(self.sub_collection_teach).document(id).get()._reference.set({
            "tweet_state": "delete",
        }, merge=True)
        return True


user_log_instance = UserLogService()
