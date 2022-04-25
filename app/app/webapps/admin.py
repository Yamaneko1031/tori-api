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

# router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
router = APIRouter(include_in_schema=False)

tag_service = services.tag_instance
word_service = services.word_instance
user_log_service = services.user_log_instance
system_service = services.system_instance

@router.get("/admin")
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
    
    items = []
    if "selsected_items" in result._dict:
        items = re.sub('(\[|\'|\]|\s)', '', result._dict["selsected_items"]).split(',')
        print(items)

        if result._dict["action"] == "ip_watch":
            pass
        
        elif result._dict["action"] == "delete_tweet":
            for item in items:
                log_data = user_log_service.get_teach_log(year, month, day, item)
                if log_data["tweet_state"] == "tweet":
                    word_service.delete_tweet(log_data["tweet_id"])
                    user_log_service.update_teach_log_tweet_delete(
                        year, month, day, item)
                else:
                    print("削除済み")
                    
        elif result._dict["action"] == "ip_restriction":
            for item in items:
                log_data = user_log_service.get_teach_log(year, month, day, item)
                system_service.add_ng_ip(log_data["ip_address"])
            word_service.renew_ng_list()
                
        elif result._dict["action"] == "session_restriction":
            for item in items:
                log_data = user_log_service.get_teach_log(year, month, day, item)
                system_service.add_ng_session(log_data["session_id"])
            word_service.renew_ng_list()
                
        elif result._dict["action"] == "delete_word":
            for item in items:
                log_data = user_log_service.get_teach_log(year, month, day, item)
                word_service.delete_from_ref(log_data["word_ref"])
                
        elif result._dict["action"] == "update_mean":
            for item in items:
                log_data = user_log_service.get_teach_log(year, month, day, item)
                word_service.update_mean(log_data["word"], result._dict["mean"], "admin")
                
        elif result._dict["action"] == "mean_init":
            for item in items:
                log_data = user_log_service.get_teach_log(year, month, day, item)
                word_service.update_mean(log_data["word"], log_data["word"], "admin")
                
        else:
            pass

    ret_teach_logs = user_log_service.get_teach_logs(year, month, day)
    date = {"year": year, "month": month, "day": day}
    return templates.TemplateResponse("log_teach.html", {"request": request, "data": ret_teach_logs, "date": date, "result": result})


@router.get("/admin/word_list")
@router.post("/admin/word_list")
async def admin_word_list(request: Request):
    result = await request.form()
    print(result)
    
    items = []
    if "selsected_items" in result._dict:
        items = re.sub('(\[|\'|\]|\s)', '', result._dict["selsected_items"]).split(',')
        print(items)
        
    next_key = None
    if "action" in result._dict:
        if result._dict["action"] == "next":
            if result._dict["next_key"] != 'None':
                print(result._dict["next_key"])
                date_time = datetime.fromisoformat(str(result._dict["next_key"]))
                next_key = DatetimeWithNanoseconds(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond)
                
        elif result._dict["action"] == "fitst":
            pass
        
        elif result._dict["action"] == "delete_word":
            for item in items:
                word_service.delete(item)
            
        elif result._dict["action"] == "mean_init":
            for item in items:
                word_service.update_mean(item, item, "admin")
            
        elif result._dict["action"] == "update_mean":
            for item in items:
                word_service.update_mean(item, result._dict["mean"], "admin")
                
        elif result._dict["action"] == "update_tag":
            for item in items:
                tags_cnt_dict = json.loads(result._dict["tags_cnt"].replace("'", '"'))
                word_service.update_tags(item, tags_cnt_dict)

    word_list = word_service.get_word_list_next(20, next_key)
    # print(word_list["doc"])

    return templates.TemplateResponse("word_list.html", {"request": request, "data": word_list})


@router.get("/admin/ng_word")
@router.post("/admin/ng_word")
async def admin(request: Request):
    result = await request.form()
    # print(result._dict)
    if "arr" in result._dict:
        arr2 = re.sub('(\[|\'|\]|\s)', '', result._dict["arr"]).split(',')
        print(arr2)
    return templates.TemplateResponse("ng_word.html", {"request": request})