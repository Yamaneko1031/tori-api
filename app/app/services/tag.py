from uuid import UUID
from datetime import datetime
import random
from google.cloud.firestore_v1 import collection
from typing import List

import jaconv
from google.cloud import firestore

from app import models, services

db = firestore.Client()

system_service = services.system_instance


class TagService:

    def __init__(self):
        self.coices = []
        colection = db.collection("tag_choices")
        docs = colection.stream()
        for doc in docs:
            self.coices.append(doc.to_dict()["list"])

    # collection_name = [
    #     "tags1",
    #     "tags2",
    # ]

    # def use_tag(self, word: str, kind: int):
    #     colection = db.collection(self.collection_name[kind])
    #     doc_ref = colection.document(word)
    #     if not doc_ref.get().exists:
    #         return False
    #     doc_ref.update({
    #         "used": firestore.Increment(1),
    #         "updated_at": datetime.utcnow(),
    #     })
    #     return True

    # def get_tags(self, kind: int):
    #     colection = db.collection(self.collection_name[kind])
    #     docs = colection.order_by("updated_at", direction=firestore.Query.DESCENDING).stream()
    #     data = []
    #     for doc in docs:
    #         tmp = doc.to_dict()
    #         del tmp["updated_at"], tmp["used"]
    #         data.append(tmp)

    #     return data

    # def get_total_pnt(self, tags: List[str]) -> int:
    #     for tag in tags:
    #         get_tag()

    def create_tag(self, base: str, part: str, pnt: int, text: str, kana: str):
        colection_act = db.collection("act_tags")
        colection_act.document(base).set({
            "part": part,
            "pnt": pnt,
            "text": text
        })

        colection_called = db.collection("called_tags")
        colection_called.document(base).set({
            "refer": colection_act.document(base)
        })
        if base != kana:
            colection_called.document(kana).set({
                "refer": colection_act.document(base)
            })

    def create_reserve_tags(self, base: str, part: str, pnt: int, text: str, kana: str):
        colection_act = db.collection("reserve_tags")
        colection_act.document(base).set({
            "part": part,
            "pnt": pnt,
            "text": text,
            "kana": kana
        })

    def create_tag_from_reserve(self, doc_name: str, pnt: int):
        doc = db.collection(
            "reserve_tags").document(doc_name).get()
        if doc.exists:
            data = doc.to_dict()
            self.create_tag(doc_name, data["part"],
                            pnt, data["text"], data["kana"])
            db.collection("reserve_tags").document(doc_name).delete()

    def get_tag(self, tag: str, get_ref: bool = False):
        """ タグの情報を取得する
        """
        collection = db.collection("called_tags")
        # カタカナはひらがなにする
        tag = jaconv.kata2hira(tag)

        doc = collection.document(tag).get()

        if doc.exists:
            if get_ref:
                return doc.to_dict()["refer"]

            return doc.to_dict()["refer"].get().to_dict()

        return

    def get_random_choices(self):
        """ ランダムな選択肢を取得する
        """
        ret_data = []
        coices = random.choice(self.coices)
        for key in coices:
            ret_data.append(self.get_tag(key))

        return ret_data

    def get_random_tag_more0(self):
        """ pnt0以上のタグを取得する
        """
        tag_more0 = []
        docs = db.collection("act_tags").where("pnt", ">=", 0).stream()
        for doc in docs:
            tag_more0.append(doc.to_dict())

        return random.choice(tag_more0)


tag_instance = TagService()
