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
    # sub_collection_mean_update = "mean_update_log"

    def __init__(self):
        """ コンストラクタ
        """
        return


    def add_teach_log(self, word: str, mean: str, ip_adress: str, session_id: str, tweet_state: str, tweet_id: int):
        day_ref = db.collection(
            self.collection_name).document(datetime.today().strftime("%Y-%m-%d"))
        doc = day_ref.collection(self.sub_collection_teach).document()
        doc.set({
            "action": "新規",
            "word": word,
            "mean": mean,
            "pre_mean": "",
            "ip_address": ip_adress,
            "tweet_state": tweet_state,
            "tweet_id": tweet_id,
            "session_id": session_id,
            "created_at": datetime.utcnow()
        })
        
        return doc.id
        
        
    def add_mean_update_log(self, word: str, mean: str, pre_mean: str, ip_adress: str, session_id: str, tweet_state: str, tweet_id: int):
        day_ref = db.collection(
            self.collection_name).document(datetime.today().strftime("%Y-%m-%d"))
        doc = day_ref.collection(self.sub_collection_teach).document()
        doc.set({
            "action": "意味更新",
            "word": word,
            "mean": mean,
            "pre_mean": pre_mean,
            "ip_address": ip_adress,
            "tweet_state": tweet_state,
            "tweet_id": tweet_id,
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
            data["created_at"] = data["created_at"].strftime("%Y/%m/%d %H:%M:%S")
            data["id"] = doc.id
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