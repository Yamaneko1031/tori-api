from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from datetime import datetime


class UaerBase(BaseModel):
    name: str
    age: int


class UserCreate(UaerBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserUpdate(UaerBase):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class User(UaerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
