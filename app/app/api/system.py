from datetime import datetime
import random
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, Request
from google.cloud import firestore

# from app import models, services

router = APIRouter()


@router.get("/session", tags=["system"])
def get_session(request: Request):
    print("request.headers:{}".format(request.headers))
    db = firestore.Client()
    sessions = db.collection('sessions')
    session_id = ""
    if 'session_id' in request.headers:
        session_id = request.headers["session_id"]
    if session_id == "":
        session_id = str(uuid4())
        doc_ref = sessions.document(document_id=session_id)
        data = {}
        data["created_at"] = datetime.utcnow()
        doc_ref.set(data)

    return {"session_id": session_id}
