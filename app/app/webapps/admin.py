from datetime import date, datetime
import json
from termios import PARODD
from typing import Optional
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


@router.post("/admin/log/day")
async def admin(request: Request):
    # result = request.form()
    result = await request.form()
    print(result._dict)

    year = int(result._dict["year"])
    month = int(result._dict["month"])
    day = int(result._dict["day"])
    
    if result._dict["kind"] == "teach":
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
                        word_service.tweet_delete(log_data["tweet_log"])
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

    elif result._dict["kind"] == "action":
    
        ret_action_logs = user_log_service.get_action_logs(year, month, day)
        date = {"year": year, "month": month, "day": day}
        return templates.TemplateResponse("log_action.html", {"request": request, "data": ret_action_logs, "date": date, "result": result})
    
    
    return templates.TemplateResponse("log_calendar.html", {"request": request})


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
    
    if "action" in result._dict:
        if result._dict["action"] == "add_ng":
            system_service.add_ng_list(word_service.check_text_conv(result._dict["input"]))
        elif result._dict["action"] == "delete_ng":
            system_service.delete_ng_list(result._dict["input"])
            
        word_service.renew_ng_list()
    
    ng_list = system_service.get_ng_list()
    
    return templates.TemplateResponse("ng_word.html", {"request": request, "data": ng_list})


@router.get("/admin/ng_regex")
@router.post("/admin/ng_regex")
async def admin(request: Request):
    result = await request.form()
    # print(result._dict)
    
    if "action" in result._dict:
        if result._dict["action"] == "add_ng":
            system_service.add_ng_regex(result._dict["input"])
        elif result._dict["action"] == "delete_ng":
            system_service.delete_ng_regex(result._dict["input"])
            
        word_service.renew_ng_list()
    
    ng_list = system_service.get_ng_regex()
    
    return templates.TemplateResponse("ng_regex.html", {"request": request, "data": ng_list})


@router.get("/admin/ng_session")
@router.post("/admin/ng_session")
async def admin(request: Request):
    result = await request.form()
    # print(result._dict)
    
    if "action" in result._dict:
        if result._dict["action"] == "add_ng":
            system_service.add_ng_session(result._dict["input"])
        elif result._dict["action"] == "delete_ng":
            system_service.delete_ng_session(result._dict["input"])
            
        word_service.renew_ng_list()
    
    ng_list = system_service.get_ng_session()
    
    return templates.TemplateResponse("ng_session.html", {"request": request, "data": ng_list})


@router.get("/admin/ng_ip")
@router.post("/admin/ng_ip")
async def admin(request: Request):
    result = await request.form()
    # print(result._dict)
    
    if "action" in result._dict:
        if result._dict["action"] == "add_ng":
            system_service.add_ng_ip(result._dict["input"])
        elif result._dict["action"] == "delete_ng":
            system_service.delete_ng_ip(result._dict["input"])
            
        word_service.renew_ng_list()
    
    ng_list = system_service.get_ng_ip()
    
    return templates.TemplateResponse("ng_ip.html", {"request": request, "data": ng_list})


@router.get("/admin/tweet_log")
@router.post("/admin/tweet_log")
async def admin_tweet_log(request: Request):
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
        
        elif result._dict["action"] == "delete_tweet":
            for item in items:
                word_service.tweet_delete(item)
            
        elif result._dict["action"] == "force_tweet":
            for item in items:
                word_service.tweet_force(item)
                

    tweet_list = word_service.get_tweet_log_next(20, next_key)
    # print(word_list["doc"])

    return templates.TemplateResponse("tweet_log.html", {"request": request, "data": tweet_list})









import os
from requests_oauthlib import OAuth1Session
from fastapi.responses import RedirectResponse
from fastapi import Response, Cookie
from urllib.parse import parse_qsl

@router.get("/oauth_url")
async def oauth_url(response: Response):
        
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']

    base_url = 'https://api.twitter.com/'

    request_token_url = base_url + 'oauth/request_token'
    authenticate_url = base_url + 'oauth/authenticate'
    access_token_url = base_url + 'oauth/access_token'
    authorize_url = base_url + 'oauth/authorize'

    base_json_url = 'https://api.twitter.com/1.1/%s.json'
    user_timeline_url = base_json_url % ('statuses/user_timeline')
    
    # response.set_cookie(key="fakesession", value="fake-cookie-session-value")


    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret)
    # url = 'https://api.oauth_client.com/1/account/settings.json'
    # response = oauth_client.get(url)

    # fetch_response = oauth_client.fetch_request_token(request_token_url)
    # resource_owner_key = fetch_response.get('oauth_token')
    # resource_owner_secret = fetch_response.get('oauth_token_secret')
    
    # response.set_cookie("resource_owner_key", fetch_response.get('oauth_token'))
    # response.set_cookie("resource_owner_secret", fetch_response.get('oauth_token_secret'))
    
    # url = oauth_client.authorization_url(authorize_url)
    
    resp = oauth_client.post(
        request_token_url,
        params={'oauth_callback': "https://torichan.app"}
    )

    # responseからリクエストトークンを取り出す
    request_token = dict(parse_qsl(resp.content.decode("utf-8")))

    # リクエストトークンから連携画面のURLを生成
    authenticate_url = "https://api.twitter.com/oauth/authenticate"
    authenticate_endpoint = '%s?oauth_token=%s' \
        % (authenticate_url, request_token['oauth_token'])
        
    print(request_token['oauth_token'])
    print(request_token['oauth_token_secret'])
    
    # response.delete_cookie("resource_owner_key", path='/', domain=None)
    # response.delete_cookie("resource_owner_secret", path='/', domain=None)
    
    response.set_cookie(key="resource_owner_key", value=request_token['oauth_token'], expires=60*60*24*7)
    response.set_cookie(key="resource_owner_secret", value=request_token['oauth_token_secret'], expires=60*60*24*7)
    
    # return "BBB"
    return authenticate_endpoint


@router.get("/oauth_test3")
async def oauth_test3(resource_owner_key: Optional[str] = Cookie(None), resource_owner_secret: Optional[str] = Cookie(None)):
    print(resource_owner_key)
    print(resource_owner_secret)
    return "aaaaa"
    
    
@router.get("/oauth_test2")
async def oauth_test2(resource_owner_key: Optional[str] = Cookie(None), resource_owner_secret: Optional[str] = Cookie(None)):
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    base_url = 'https://api.twitter.com/'
    access_token_url = base_url + 'oauth/access_token'
        
    print(resource_owner_key)
    print(resource_owner_secret)
    
    oauth_token = resource_owner_key
    oauth_token_secret = resource_owner_secret
    oauth_verifier = 'VTQUdzcefUXqVKmjGG5yUtFducaOp3Nm'
    
    oauth_client = OAuth1Session(consumer_key,
                                 client_secret=consumer_secret,
                                 resource_owner_key=oauth_token,
                                #  resource_owner_secret=oauth_token_secret,
                                 verifier=oauth_verifier)
    
    # response = oauth_client.post(
    #     access_token_url,
    #     params={'oauth_verifier': oauth_verifier}
    # )
    # access_token = dict(parse_qsl(response.content.decode("utf-8")))
    
    oauth_tokens = oauth_client.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    
    resource_owner_user_id = oauth_tokens.get('user_id')
    resource_owner_screen_name = oauth_tokens.get('screen_name')

    print(resource_owner_key)    # レスポンスのHTMLを文字列で取得
    print(resource_owner_secret)    # レスポンスのHTMLを文字列で取得
    print(resource_owner_user_id)
    print(resource_owner_screen_name)

    # oauth_client.post()


    # access_endpoint_url = "https://api.twitter.com/oauth/access_token"

    # session_acc = OAuth1Session(API_KEY, API_KEY_SECRET, oauth_token, oauth_verifier)
    # response_acc = session_acc.post(access_endpoint_url, params={"oauth_verifier": oauth_verifier})
    # response_acc_text = response_acc.text

    # access_token_kvstr = response_acc_text.split("&")
    # acc_token_dict = {x.split("=")[0]: x.split("=")[1] for x in access_token_kvstr}
    # access_token = acc_token_dict["oauth_token"]
    # access_token_secret = acc_token_dict["oauth_token_secret"]

    # print("Access Token       :", access_token)
    # print("Access Token Secret:", access_token_secret)
    # print("User ID            :", acc_token_dict["user_id"])
    # print("Screen Name        :", acc_token_dict["screen_name"])






    # access_token = {
    #     'oauth_token': "アクセストークンの中のoauth_token",
    #     'oauth_token_secret': "アクセストークンの中のoauth_token_secret",
    # }

    # params = {
    #     'user_id': "アクセストークンの中のuser_id",
    #     'exclude_replies': True,
    #     'include_rts': json.get('include_rts', False),
    #     'count': 20,
    #     'trim_user': False,
    #     'tweet_mode': 'extended',    # full_textを取得するために必要
    # }

    # twitter = OAuth1Session(
    #     consumer_key,
    #     consumer_secret,
    #     resource_owner_key,
    #     resource_owner_secret,
    # )
    # api = twitter.Api(consumer_key=_CONSUMER_KEY,
    #                   consumer_secret=_CONSUMER_SECRET,
    #                   access_token_key=resp.get('oauth_token'),
    #                   access_token_secret=resp.get('oauth_token_secret'))
 
    # tw_user = api.VerifyCredentials()
    
    # response = twitter.get(user_timeline_url, params=params)
    # results = json.loads(response.text)

    # print(results)


    return "aaaa"
