import re
from app.services.system import SystemService
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi import Form
from fastapi.templating import Jinja2Templates

from app import models, services

router = APIRouter()

tag_service = services.tag_instance
word_service = services.word_instance
user_log_service = services.user_log_instance
system_service = services.system_instance

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(include_in_schema=False)

@router.get("/admin")
def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@router.get("/admin/{year}/{month}/{day}")
def admin(request: Request, year: int, month: int, day: int):
    ret_word = word_service.get_one_day_learn_words(year, month, day)
    ret_teach_logs = user_log_service.get_teach_logs(year, month, day)
    # s = word["word"]
    # m = re.match(r'([a-z]+)@([a-z]+)\.com', s)
    # jaconv.kata2hira(word1)
    # print(request.client.host)
    # for word in ret_word:
    #     if re.match(r'.*た.*く.*っ.*ち.*', word['word']):
    #         print(word["word"])
    date = {"year": year,"month": month,"day": day}
    return templates.TemplateResponse("learn_word.html", {"request": request, "data": ret_teach_logs, "date": date})

@router.post("/admin/{year}/{month}/{day}")
async def admin(request: Request, year: int, month: int, day: int):
    # result = request.form()
    result = await request.form()
    print(result._dict)
    if "id" in result:
        log_data = user_log_service.get_teach_log(year, month, day, result._dict["id"])

        if result._dict["action"] == "ip_watch":
            pass
        elif result._dict["action"] == "delete_tweet":
            if log_data["tweet_state"] == "tweet":
                word_service.delete_tweet(log_data["tweet_id"])
                user_log_service.update_teach_log_tweet_delete(year, month, day, result._dict["id"])
            else:
                print("削除済み")
            pass
        elif result._dict["action"] == "ip_restriction":
            system_service.add_ng_ip(log_data["ip_address"])
            pass
        else:
            pass
        
    ret_teach_logs = user_log_service.get_teach_logs(year, month, day)
    date = {"year": year,"month": month,"day": day}
    return templates.TemplateResponse("learn_word.html", {"request": request, "data": ret_teach_logs, "date": date, "result": result})


@router.get("/admin/search/word/{word}")
def admin(request: Request, word: str):
    return templates.TemplateResponse("learn_word.html", {"request": request, "data": ret_teach_logs})
