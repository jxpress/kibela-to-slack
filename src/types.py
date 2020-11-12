from typing import Any, Optional
from pydantic import BaseModel


class Config(BaseModel):
    pretext: Optional[str]
    edit_comment: Optional[Any]
    folder: Optional[str]
    title: Optional[str]
    channel: Optional[str]
    preserve_comments: Optional[Any]
    skip_draft: Optional[Any]


class Item(BaseModel):
    title: Optional[str]
    text: str
    folder: Optional[str]
    group: Optional[str]
    edit_comment: Optional[str]
    author_name: str
