from fastapi import APIRouter, Body, HTTPException

from app import models, services

router = APIRouter()

user_service = services.UserService()


@router.post("/users", response_model=models.User, tags=["user"])
def create_user(user_create: models.UserCreate):
    return user_service.create(user_create)


@router.get("/users/{id}", response_model=models.User, tags=["user"])
def get_user_from_id(id: str):
    user = user_service.get_from_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.get("/users/session/{id}", response_model=models.User, tags=["user"])
def get_user_from_session(id: str):
    user = user_service.get_from_session(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.put("/users/taught/{id}", response_model=models.User, tags=["user"])
def add_taught_word(id: str, taught_word: models.TaughtWord):
    ret = user_service.add_taught_word(id, taught_word)
    if not ret:
        raise HTTPException(status_code=404, detail="User not found.")
    return True


@router.put("/users/{id}", response_model=models.User, tags=["user"])
def update_user(id: str, user_update: models.UserUpdate):
    user = user_service.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user_service.update_user(id, user_update)


@router.delete("/users/{id}", response_model=models.User, tags=["user"])
def delete_user(id: str):
    user = user_service.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user_service.delete(id)



# import os
# from requests_oauthlib import OAuth1Session
# from fastapi.responses import RedirectResponse
# from fastapi import Response, Cookie
# from urllib.parse import parse_qsl

# @router.get("/oauth_url")
# async def oauth_url():
        
#     consumer_key = os.environ['CONSUMER_KEY']
#     consumer_secret = os.environ['CONSUMER_SECRET']

#     base_url = 'https://api.twitter.com/'

#     request_token_url = base_url + 'oauth/request_token'
#     authenticate_url = base_url + 'oauth/authenticate'
    
#     oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret)
        
#     resp = oauth_client.post(
#         request_token_url,
#         params={'oauth_callback': "https://torichan.app"}
#     )

#     # responseからリクエストトークンを取り出す
#     request_token = dict(parse_qsl(resp.content.decode("utf-8")))

#     # リクエストトークンから連携画面のURLを生成
#     authenticate_url = "https://api.twitter.com/oauth/authenticate"
#     authenticate_endpoint = '%s?oauth_token=%s' \
#         % (authenticate_url, request_token['oauth_token'])
    
#     return authenticate_endpoint

    
# @router.post("/create_temp_fromt", tags=["word"])
# def create_temp_fromt(word: str, cnt: int, session_id: Optional[str] = Header(None)):
#     """ フロント側から情報をテンポラリに保存
#     """
#     set_id = "{}{}".format(session_id, cnt)
#     id = word_service.create_temp_fromt(word, set_id)
#     if not id:
#         raise HTTPException(status_code=404, detail="Not found.")
#     return {"detail": "success"}



# @router.get("/oauth_session")
# async def oauth_test2(oauth_token: str, oauth_verifier: str):
#     consumer_key = os.environ['CONSUMER_KEY']
#     consumer_secret = os.environ['CONSUMER_SECRET']
#     base_url = 'https://api.twitter.com/'
#     access_token_url = base_url + 'oauth/access_token'    
    
#     oauth_client = OAuth1Session(consumer_key,
#                                  client_secret=consumer_secret,
#                                  resource_owner_key=oauth_token,
#                                  verifier=oauth_verifier)
    
#     # response = oauth_client.post(
#     #     access_token_url,
#     #     params={'oauth_verifier': oauth_verifier}
#     # )
#     # access_token = dict(parse_qsl(response.content.decode("utf-8")))
    
#     oauth_tokens = oauth_client.fetch_access_token(access_token_url)
#     resource_owner_key = oauth_tokens.get('oauth_token')
#     resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    
#     resource_owner_user_id = oauth_tokens.get('user_id')
#     resource_owner_screen_name = oauth_tokens.get('screen_name')

#     print(resource_owner_key)    # レスポンスのHTMLを文字列で取得
#     print(resource_owner_secret)    # レスポンスのHTMLを文字列で取得
#     print(resource_owner_user_id)
#     print(resource_owner_screen_name)

#     return "aaaa"
