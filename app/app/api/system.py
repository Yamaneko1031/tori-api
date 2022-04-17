from typing import Optional
from datetime import datetime
import random
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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


@router.put("/reset_tweet_cnt", tags=["system"])
def reset_tweet_cnt():
    return system_service.reset_tweet_cnt()


# from starlette.routing import Router
# static_router = Router()
# app.mount("/static", other_router)

# static_router.mount("/static", StaticFiles(directory="app/static"), name="static")
# templates = Jinja2Templates(directory="app/templates")

# @static_router.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     print(id)
#     print(templates)
#     data = {"request": request, "id": "aaa", "test": "aaf534dgfa"}
#     return templates.TemplateResponse("item.html", data)
