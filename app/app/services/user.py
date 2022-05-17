from uuid import UUID

import os
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl

from google.cloud import firestore

from app import models, services

db = firestore.Client()

class UserService:
    collection_name = "users"
    sub_collection_taught = "words"
    twitter_api_base = 'https://api.twitter.com/'


    def create(self, user_create: models.UserCreate) -> models.User:
        data = user_create.dict()
        doc_ref = db.collection(
            self.collection_name).document(user_create.twitter_id)
        doc_ref.set(data)
        return self.get_from_id(user_create.twitter_id)


    def get_from_id(self, id: str) -> models.User:
        doc_ref = db.collection(self.collection_name).document(id)
        doc = doc_ref.get()
        if doc.exists:
            return models.User(**doc.to_dict())
        return


    def get_from_session(self, session_id: str) -> models.User:
        docs = db.collection(self.collection_name).where(
            "session_id", "==", session_id).limit(1).get()
        if docs:
            return models.User(**docs[0].to_dict())
        return
    
    
    def add_taught_word(self, id: str, taught_word: models.TaughtWord) -> bool:
        doc_ref = db.collection(self.collection_name).document(id)
        if doc_ref:
            doc = doc_ref.collection(self.sub_collection_taught).document()
            doc.set(taught_word.dict())
            return True
        return
    
    
    def update(self, id: str, user_update: models.UserUpdate) -> models.User:
        data = user_update.dict()
        doc_ref = db.collection(self.collection_name).document(id)
        doc_ref.update(data)
        return self.get(id)


    def delete(self, id: str) -> None:
        db.collection(self.collection_name).document(id).delete()


    def get_oauth_url(self) -> str:
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']

        request_token_url = self.twitter_api_base + 'oauth/request_token'
        authenticate_url = self.twitter_api_base + 'oauth/authenticate'
        
        oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret)
            
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
        
        return authenticate_endpoint

       
    def oauth_login(self, oauth_token: str, oauth_verifier: str, session_id: str) -> models.User:
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        access_token_url = self.twitter_api_base + 'oauth/access_token'    
        
        oauth_client = OAuth1Session(consumer_key,
                                    client_secret=consumer_secret,
                                    resource_owner_key=oauth_token,
                                    verifier=oauth_verifier)
        
        oauth_tokens = oauth_client.fetch_access_token(access_token_url)
        
        user = self.get_from_id(oauth_tokens.get('user_id'))
        
        if user:
            return user
        else:
            user_data = models.UserCreate()
            user_data.twitter_id = oauth_tokens.get('user_id')
            user_data.twitter_name= oauth_tokens.get('screen_name')
            user_data.twitter_key= oauth_tokens.get('oauth_token')
            user_data.twitter_secret= oauth_tokens.get('oauth_token_secret')
            user_data.session_id = session_id
            return self.create(user_data.dict())


user_instance = UserService()
        
        
# class UaerBase(BaseModel):
#     name: str
#     age: int


# class UserCreate(UaerBase):
#     twitter_id: str
#     twitter_name: str
#     twitter_key: str
#     twitter_secret: str
#     id: UUID = Field(default_factory=uuid4)
#     created_at: datetime = Field(default_factory=datetime.now)
#     updated_at: datetime = Field(default_factory=datetime.now)
    
    
        
#     def create(self, user_create: models.UserCreate) -> models.User:
#         data = user_create.dict()
#         data["id"] = str(data["id"])
#         doc_ref = db.collection(
#             self.collection_name).document(str(user_create.id))
#         doc_ref.set(data)
#         return self.get(user_create.id)
    
#         print(resource_owner_key)    # レスポンスのHTMLを文字列で取得
#         print(resource_owner_secret)    # レスポンスのHTMLを文字列で取得
#         print(resource_owner_user_id)
#         print(resource_owner_screen_name)
        
        
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

#     return "aaaa"
