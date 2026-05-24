from fastapi import FastAPI

from routers import comments, posts, summarys
from database import create_db_and_tables

# FastAPI 인스턴스 생성
app = FastAPI()


# DB 연결 - 앱 시작시 테이블 생성
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# 라우터 연결
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(summarys.router)


# 루트 페이지
@app.get("/")
async def root():
    return {"message": "Hello! Bigger Community!"}
