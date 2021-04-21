from typing import Optional
from datetime import datetime
import random
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, Header, Request
from google.cloud import firestore

from app import models, services

router = APIRouter()

system_service = services.system_instance


@router.get("/info", tags=["system"])
def get_session(request: Request):
    ret_data = system_service.get_system_data()
    if not ret_data:
        raise HTTPException(status_code=404, detail="unknown info.")
    return ret_data


@router.put("/janken", tags=["system"])
def add_janken_result(result: int, session_id: Optional[str] = Header(None)):
    if system_service.add_janken_result(result, session_id):
        return {"detail": "success"}
    else:
        raise HTTPException(status_code=404, detail="param error.")


@router.get("/janken", tags=["system"])
def add_janken_result():
    return system_service.get_janken_result_total()

