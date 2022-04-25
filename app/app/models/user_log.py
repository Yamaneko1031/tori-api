from typing import Dict, List
# from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from datetime import datetime


class BaseTeachLog(BaseModel):
    def __init__(self, word: str, mean: str, ip_adress: str, session_id: str):
        self.word = word
        self.mean = mean
        self.ip_adress = ip_adress
        self.session_id = session_id

    word: str = ""
    mean: str = ""
    ip_address: str = ""
    session_id: str = ""


class TeachLogCreate(BaseTeachLog):
    pass


class TeachLogAll(BaseTeachLog):
    created_at: datetime = Field(default_factory=datetime.now)
