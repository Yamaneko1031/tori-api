# from typing import List

# from pydantic import BaseModel, Field
# from datetime import datetime


# class BaseCategory(BaseModel):
#     word: str = ""


# class CategoryCreate(BaseCategory):
#     pass


# class CategoryUpdate(BaseCategory):
#     raiting: int
#     pass


# class CategoryAll(BaseCategory):
#     cnt: int = 0
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)
