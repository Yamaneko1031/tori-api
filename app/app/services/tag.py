from uuid import UUID
from datetime import datetime

from google.cloud import firestore

from app import models, services

db = firestore.Client()
# system_service = services.SystemService()
system_service = services.system_instance

class TagService:
    collection_name = [
        "tags1",
        "tags2",
    ]

    def use_tag(self, word: str, kind: int):
        colection = db.collection(self.collection_name[kind])
        doc_ref = colection.document(word)
        if not doc_ref.get().exists:
            return False
        doc_ref.update({
            "used": firestore.Increment(1),
            "updated_at": datetime.utcnow(),
        })
        return True

    def get_tags(self, kind: int):
        colection = db.collection(self.collection_name[kind])
        docs = colection.order_by("updated_at", direction=firestore.Query.DESCENDING).stream()
        data = []
        for doc in docs:
            tmp = doc.to_dict()
            del tmp["updated_at"], tmp["used"]
            data.append(tmp)

        return data


tag_instance = TagService()