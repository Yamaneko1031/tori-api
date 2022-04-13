import re
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates

from app import models, services

router = APIRouter()

tag_service = services.tag_instance
word_service = services.word_instance

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(include_in_schema=False)

@router.get("/admin")
def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@router.get("/admin/{year}/{month}/{day}")
def admin(request: Request, year: int, month: int, day: int):
    ret_word = word_service.get_one_day_learn_words(year, month, day)
    # s = word["word"]
    # m = re.match(r'([a-z]+)@([a-z]+)\.com', s)
    # jaconv.kata2hira(word1)
    # print(request.client.host)
    # for word in ret_word:
    #     if re.match(r'.*た.*く.*っ.*ち.*', word['word']):
    #         print(word["word"])
    return templates.TemplateResponse("learn_word.html", {"request": request, "data": ret_word, "ip": request.client.host})
