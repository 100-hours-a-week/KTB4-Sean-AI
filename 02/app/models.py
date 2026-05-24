from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


# --- SQLModel 테이블 모델 (실제 DB 테이블) ---
class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    username: str
    created_at: datetime = Field(default_factory=datetime.now)


class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    content: str
    username: str
    created_at: datetime = Field(default_factory=datetime.now)


# --- Pydantic 스키마 (Request / Response) ---
# 게시글
class PostCreate(BaseModel):
    title: str
    content: str
    username: str


class PostUpdate(BaseModel):
    title: str | None
    content: str | None


# 댓글
class CommentCreate(BaseModel):
    content: str
    username: str


class CommentUpdate(BaseModel):
    content: str | None


# 요약
class PostSummaryResponse(BaseModel):
    post_id: int
    summary: str
