from typing import List
# from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from datetime import datetime


class BaseWord(BaseModel):
    word: str = ""
    mean: str = ""

class WordCreate(BaseWord):
    pass


class WordUpdate(BaseWord):
    raiting: int
    pass


class WordAll(BaseWord):
    good: int = 0
    bad: int = 0
    cnt: int = 0
    kind: str = ""
    tag1: List[str] = []
    tag2: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tweeted_at: datetime = datetime(1, 1, 1)


class WordAddTag(BaseModel):
    word: str = ""
    tag: str = ""