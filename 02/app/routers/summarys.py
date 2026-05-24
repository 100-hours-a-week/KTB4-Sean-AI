from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ollama import chat

from database import SessionDep
from models import Post

router = APIRouter(tags=["AI 요약"])


@router.post("/posts/{post_id}/summary")
async def summarize(post_id: int, session: SessionDep):
    # 1. DB에서 게시글 조회 (없으면 404)
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="요약할 게시글을 찾을 수 없습니다.")

    # 2. summarize_post 함수 호출
    summary = summarize_post(post.title, post.content)

    # 3. 결과 반환
    return JSONResponse(
        content={
            "status": "Summary Created Successfully",
            "message": "요약 생성 완료",
            "data": summary,
        },
        status_code=201,
    )


def summarize_post(title: str, content: str) -> str:

    # 1. 프롬프트 구성
    prompt = f"다음 게시글을 한국어로 딱 한문장으로 간결하게 정리해줘. 제목 : {title}, 본문: {content}"

    # 2. Ollama 호출
    response = chat(
        model="gemma3",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.message.content
