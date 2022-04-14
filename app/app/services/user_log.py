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
            self.collection_name).document(datetime.today().strftime("%y-%m-%d"))
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
            self.collection_name).document(datetime.today().strftime("%y-%m-%d"))
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
    
user_log_instance = UserLogService()