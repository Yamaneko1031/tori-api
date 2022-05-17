from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from datetime import datetime


class UaerBase(BaseModel):
    twitter_id: str = ""
    twitter_name: str = ""
    session_id: str = ""


class UserCreate(UaerBase):
    twitter_key: str = ""
    twitter_secret: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
            
        
class UserUpdate(UaerBase):
    updated_at: datetime = Field(default_factory=datetime.now)


class User(UaerBase):
    created_at: datetime
    updated_at: datetime


class TaughtWord(BaseModel):
    word: str = ""
    mean: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
