from ninja import Schema
from datetime import datetime


class CommentCreateSchema(Schema):
    article_id: int
    text: str


class CommentUpdateSchema(Schema):
    text: str


class CommentOutSchema(Schema):
    id: int
    author_id: int
    article_id: int
    text: str
    created_at: datetime
    updated_at: datetime
