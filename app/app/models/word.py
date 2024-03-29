from typing import Dict, List
# from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from datetime import datetime


class BaseWord(BaseModel):
    word: str = ""
    mean: str = ""

class WordCreate(BaseWord):
    kind: str = ""
    secret_tag: str = ""
    pass


class WordUpdate(BaseWord):
    pass


class WordAll(BaseWord):
    good: int = 0
    bad: int = 0
    like: int = 0
    cnt: int = 0
    kind: str = ""
    tags: List = []
    tags_cnt: Dict = {}
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    tweeted_at: datetime = datetime(1, 1, 1)


class WordAddTag(BaseModel):
    word: str = ""
    tag: str = ""

class WordAddTagText(BaseModel):
    word: str = ""
    text: str = ""

class WordUpdateKind(BaseModel):
    word: str = ""
    kind: str = ""