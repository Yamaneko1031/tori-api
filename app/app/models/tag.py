from typing import List

from pydantic import BaseModel, Field

class TagAct(BaseModel):
    text: str = ""
    part: str = ""
    pnt: int = 0