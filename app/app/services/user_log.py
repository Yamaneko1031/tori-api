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
    sub_collection_mean_update = "mean_update_log"

    def __init__(self):
        """ コンストラクタ
        """
        return


    def add_teach_log(self, word: str, mean: str, ip_adress: str, session_id: str):
        day_ref = db.collection(
            self.collection_name).document(datetime.today().strftime("%Y-%m-%d"))
        doc = day_ref.collection(self.sub_collection_teach).document()
        doc.set({
            "word": word,
            "mean": mean,
            "ip_address": ip_adress,
            "session_id": session_id,
            "created_at": datetime.utcnow()
        })
        
        return doc.id
        
    def add_mean_update_log(self, word: str, mean: str, pre_mean: str, ip_adress: str, session_id: str):
        day_ref = db.collection(
            self.collection_name).document(datetime.today().strftime("%Y-%m-%d"))
        doc = day_ref.collection(self.sub_collection_mean_update).document()
        doc.set({
            "word": word,
            "mean": mean,
            "pre_mean": pre_mean,
            "ip_address": ip_adress,
            "session_id": session_id,
            "created_at": datetime.utcnow()
        })
        
        return doc.id
    
    def get_teach_logs(self, year: int, month: int, day: int):
        # print("{:04}-{:02}-{:02}".format(year, month, day))
        day_ref = db.collection(
            self.collection_name).document("{:04}-{:02}-{:02}".format(year, month, day))
        
        docs = day_ref.collection(self.sub_collection_teach).get()

        teach_list = []
        for doc in docs:
            teach_list.append(doc.to_dict())
        
        return teach_list
    
user_log_instance = UserLogService()