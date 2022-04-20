from datetime import date, datetime
import json
from termios import PARODD
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
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


@router.get("/admin/log/calendar")
def admin(request: Request):
    return templates.TemplateResponse("log_calendar.html", {"request": request})


@router.post("/admin/log/teach")
async def admin(request: Request):
    # result = request.form()
    result = await request.form()
    print(result._dict)

    year = int(result._dict["year"])
    month = int(result._dict["month"])
    day = int(result._dict["day"])

    if "id" in result:
        log_data = user_log_service.get_teach_log(
            year, month, day, result._dict["id"])

        if result._dict["action"] == "ip_watch":
            pass
        elif result._dict["action"] == "delete_tweet":
            if log_data["tweet_state"] == "tweet":
                word_service.delete_tweet(log_data["tweet_id"])
                user_log_service.update_teach_log_tweet_delete(
                    year, month, day, result._dict["id"])
            else:
                print("削除済み")
        elif result._dict["action"] == "ip_restriction":
            system_service.add_ng_ip(log_data["ip_address"])
            word_service.renew_ng_list()
        elif result._dict["action"] == "delete_word":
            word_service.delete_from_ref(log_data["word_ref"])
        elif result._dict["action"] == "update_mean":
            word_service.update_mean(log_data["word"], result._dict["mean"], "admin")
        else:
            pass

    ret_teach_logs = user_log_service.get_teach_logs(year, month, day)
    date = {"year": year, "month": month, "day": day}
    return templates.TemplateResponse("log_teach.html", {"request": request, "data": ret_teach_logs, "date": date, "result": result})


@router.post("/admin/word_list")
@router.get("/admin/word_list")
async def admin_word_list(request: Request):
    print("admin_word_list")
    result = await request.form()
    print(result._dict)
    
    next_key = None
    if "action" in result._dict:
        if result._dict["action"] == "next":
            pass
        
        if "word" in result:
            if result._dict["action"] == "delete_word":
                word_service.delete(result._dict["word"])
            elif result._dict["action"] == "mean_init":
                word_service.update_mean(result._dict["word"], result._dict["word"], "admin")
            elif result._dict["action"] == "update_mean":
                if result._dict["mean"]:
                    word_service.update_mean(result._dict["word"], result._dict["mean"], "admin")
            elif result._dict["action"] == "update_tag":
                tags_cnt_dict = json.loads(result._dict["tags_cnt"].replace("'", '"'))
                word_service.update_tags(result._dict["word"], tags_cnt_dict)

    if "next_key" in result._dict:
        print(result._dict["next_key"])
        date_time = datetime.fromisoformat(str(result._dict["next_key"]))
        next_key = DatetimeWithNanoseconds(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond)
                
    word_list = word_service.get_word_list_next(50, next_key)

    return templates.TemplateResponse("word_List.html", {"request": request, "data": word_list})
