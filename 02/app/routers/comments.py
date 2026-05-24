from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select

from database import SessionDep
from models import Comment, CommentCreate, CommentUpdate, Post

router = APIRouter(tags=["댓글"])


# 댓글 생성
@router.post("/posts/{post_id}/comments")
async def create_comment(post_id: int, payload: CommentCreate, session: SessionDep):
    # 게시글 존재 여부 확인
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    comment = Comment(post_id=post_id, **payload.model_dump())
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return JSONResponse(
        content={
            "status": "Created Successfully",
            "message": "댓글 생성 완료",
            "data": {
                "id": comment.id,
                "post_id": comment.post_id,
                "content": comment.content,
                "username": comment.username,
                "created_at": comment.created_at.isoformat(),
            },
        },
        status_code=201,
    )


# 특정 게시글의 댓글 전체 조회
@router.get("/posts/{post_id}/comments")
async def read_comments(post_id: int, session: SessionDep):
    # 게시글 존재 여부 확인
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    comments = session.exec(select(Comment).where(Comment.post_id == post_id)).all()
    return comments


# 특정 댓글 조회
@router.get("/posts/{post_id}/comments/{comment_id}")
async def read_comment(post_id: int, comment_id: int, session: SessionDep):
    # 게시글과 댓글 존재 여부 확인 (post_id, comment_id 체크)
    comment = session.get(Comment, comment_id)
    if not comment or comment.post_id != post_id:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    return comment


# 특정 댓글 수정
@router.patch("/posts/{post_id}/comments/{comment_id}")
async def update_comment(
    post_id: int, comment_id: int, updated: CommentUpdate, session: SessionDep
):
    # 게시글과 댓글 존재 여부 확인 (post_id, comment_id 체크)
    comment = session.get(Comment, comment_id)
    if not comment or comment.post_id != post_id:
        raise HTTPException(status_code=404, detail="수정할 댓글을 찾을 수 없습니다.")

    if updated.content is not None:
        comment.content = updated.content

    session.add(comment)
    session.commit()
    session.refresh(comment)
    return {
        "status": "Updated Successfully",
        "message": f"{comment_id}번 댓글 수정 완료",
    }


# 특정 댓글 삭제
@router.delete("/posts/{post_id}/comments/{comment_id}")
async def delete_comment(post_id: int, comment_id: int, session: SessionDep):
    comment = session.get(Comment, comment_id)
    if not comment or comment.post_id != post_id:
        raise HTTPException(status_code=404, detail="삭제할 댓글을 찾을 수 없습니다.")

    session.delete(comment)
    session.commit()
    return {
        "status": "Deleted Successfully",
        "message": f"{comment_id}번 댓글 삭제 완료",
    }
