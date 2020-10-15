from typing import Optional
from pydantic import BaseModel


class Config(BaseModel):
    pretext: Optional[str]
    edit_comment: Optional[bool]
    folder: Optional[str]
    channel: Optional[str]


class Item(BaseModel):
    title: Optional[str]
    text: str
    folder: Optional[str]
    group: Optional[str]
    edit_comment: Optional[str]
    author_name: str
