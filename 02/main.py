import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime

# FastAPI 인스턴스 생성
app = FastAPI()

# DB Inner Memory - 리스트? 딕셔너리? -> 딕셔너리가 검색 및 수정, 삭제에 더 용이
db_posts = {}
post_id_counter = 0


# 포스트 객체 구조
class PostCreate(BaseModel):
    title: str
    content: str


# 루트 페이지
@app.get("/")
async def root():
    return {"Hello! This is a Simple Community!"}


# 전체 게시글 조회
@app.get("/posts")
async def read_posts():
    return db_posts


# 특정 게시글 조회
@app.get("/posts/{post_id}")
async def read_post(post_id: int):
    return db_posts[post_id]


# 게시글 생성
@app.post("/posts")
async def create_post(payload: PostCreate):
    payload_dict = payload.model_dump()

    global post_id_counter
    post_id_counter += 1

    # 생성 로직, DB에 저장
    db_posts[post_id_counter] = payload_dict

    # json.dumps(post_dict)
    return JSONResponse(
        content={
            "message": "Created Successfully",
            "data": payload_dict,
        },
        status_code=201,
    )


# 특정 게시글 수정
@app.put("/posts/{post_id}")
async def update_post(post_id: int, updated_post: PostCreate):
    global db_posts

    if post_id in db_posts:
        # 업데이트 로직
        db_posts[post_id] = {
            "title": updated_post.title,
            "content": updated_post.content,
        }
        return {
            "status": "Updated Successfully",
            "message": f"{post_id}번 글 수정 완료",
        }
    else:
        raise HTTPException(status_code=404, detail="수정할 게시글을 찾을 수 없습니다.")


# # 특정 게시글 삭제
@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    global db_posts

    # 1. 해당 id(Key)가 존재하는지 확인 후 삭제
    if post_id in db_posts:
        del db_posts[post_id]
        return {
            "status": "Deleted Successfully",
            "message": f"{post_id}번 글 삭제 완료",
        }

    # 2. 존재하지 않으면 404 에러 반환
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
