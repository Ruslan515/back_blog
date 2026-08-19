from ninja import Schema
from datetime import datetime


class ArticleCreateSchema(Schema):
    title: str
    content: str
    category_id: int | None = None


class ArticleUpdateSchema(Schema):
    title: str | None = None
    content: str | None = None
    category_id: int | None = None


class ArticleOutSchema(Schema):
    id: int
    title: str
    content: str
    author_id: int
    category_id: int | None = None
    created_at: datetime
    updated_at: datetime
