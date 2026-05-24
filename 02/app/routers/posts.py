# 전체 게시글 조회
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select

from database import SessionDep
from models import Post, PostCreate, PostUpdate

router = APIRouter(tags=["게시글"])


# 게시글 생성
@router.post("/posts")
async def create_post(payload: PostCreate, session: SessionDep):
    post = Post(**payload.model_dump())
    session.add(post)
    session.commit()
    session.refresh(post)

    return JSONResponse(
        content={
            "status": "Created Successfully",
            "message": "글 생성 완료",
            "data": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "username": post.username,
                "created_at": post.created_at.isoformat(),
            },
        },
        status_code=201,
    )


# 전체 게시글 조회
@router.get("/posts")
async def read_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()
    return posts


# 특정 게시글 조회
@router.get("/posts/{post_id}")
async def read_post(post_id: int, session: SessionDep):
    # 게시글 존재 여부 확인
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="조회할 게시글을 찾을 수 없습니다.")
    return post


# 특정 게시글 수정
@router.patch("/posts/{post_id}")
async def update_post(post_id: int, updated_post: PostUpdate, session: SessionDep):
    # 게시글 존재 여부 확인
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="수정할 게시글을 찾을 수 없습니다.")

    # 업데이트 된 내용만 수정 (None 체크)
    if updated_post.title is not None:
        post.title = updated_post.title
    if updated_post.content is not None:
        post.content = updated_post.content

    # DB에 추가
    session.add(post)
    session.commit()
    session.refresh(post)
    return {
        "status": "Updated Successfully",
        "message": f"{post_id}번 글 수정 완료",
    }


# 특정 게시글 삭제
@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, session: SessionDep):
    # 게시글 존재 여부 확인
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="삭제할 게시글을 찾을 수 없습니다.")

    # 삭제 로직
    session.delete(post)
    session.commit()
    return {
        "status": "Deleted Successfully",
        "message": f"{post_id}번 글 삭제 완료",
    }
