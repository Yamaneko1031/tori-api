from uuid import UUID

from google.cloud import firestore

from app import models

db = firestore.Client()


class UserService:
    collection_name = "users"

    def create(self, user_create: models.UserCreate) -> models.User:
        data = user_create.dict()
        data["id"] = str(data["id"])
        doc_ref = db.collection(
            self.collection_name).document(str(user_create.id))
        doc_ref.set(data)
        return self.get(user_create.id)

    def get(self, id: UUID) -> models.User:
        doc_ref = db.collection(self.collection_name).document(str(id))
        doc = doc_ref.get()
        if doc.exists:
            return models.User(**doc.to_dict())
        return

    def update(self, id: UUID, user_update: models.UserUpdate) -> models.User:
        data = user_update.dict()
        doc_ref = db.collection(self.collection_name).document(str(id))
        doc_ref.update(data)
        return self.get(id)

    def delete(self, id: UUID) -> None:
        db.collection(self.collection_name).document(str(id)).delete()
