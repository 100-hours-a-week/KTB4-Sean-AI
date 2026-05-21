from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime

from dotenv import load_dotenv

from google import genai

# GEMINI_API_KEY를 위해 환경변수 로드
load_dotenv()


# for stream in response:
#     print(stream.text)

# FastAPI 인스턴스 생성
app = FastAPI()

# DB Inner Memory - 리스트? 딕셔너리? -> 딕셔너리가 검색 및 수정, 삭제에 더 용이
db_posts = {
    1: {
        "title": "FastAPI란?",
        "content": "FastAPI는 파이썬 기반의 매우 빠르고 현대적인 웹 프레임워크입니다. 비동기 처리를 기본으로 지원하며, Pydantic을 활용한 자동 데이터 검증과 대화형 API 문서(Swagger UI)를 자동으로 생성해 주는 강력한 장점을 지니고 있습니다.",
    },
    2: {
        "title": "LLM이란?",
        "content": "LLM은 '대규모 언어 모델(Large Language Model)'의 약자로, 방대한 양의 텍스트 데이터를 학습해 사람처럼 자연스러운 언어를 이해하고 생성하는 인공지능(AI) 기술입니다.",
    },
}
post_id_counter = max(db_posts.keys()) if db_posts else 0


# 포스트 객체 구조
class PostCreate(BaseModel):
    title: str
    content: str


# 루트 페이지
@app.get("/")
async def root():
    return {"message": "Hello! This is a Simple Community!"}


# 전체 게시글 조회
@app.get("/posts")
async def read_posts():
    return db_posts


# 특정 게시글 조회
@app.get("/posts/{post_id}")
async def read_post(post_id: int):
    if post_id not in db_posts:
        raise HTTPException(status_code=404, detail="조회할 게시글을 찾을 수 없습니다.")
    else:
        return db_posts[post_id]


# 게시글 생성
@app.post("/posts")
async def create_post(payload: PostCreate):
    payload_dict = payload.model_dump()

    global post_id_counter
    post_id_counter += 1

    # 생성 로직, DB에 저장
    db_posts[post_id_counter] = payload_dict

    return JSONResponse(
        content={
            "status": "Created Successfully",
            "message": "글 생성 완료",
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


# 특정 게시글 삭제
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


@app.post("/posts/{post_id}/summary")
async def summarize(post_id: int):
    # 1. db_posts에서 게시글 찾기 (없으면 404)
    if post_id not in db_posts:
        raise HTTPException(status_code=404, detail="요약할 게시글을 찾을 수 없습니다.")
    else:
        # title, content 받아오기
        title = db_posts[post_id]["title"]
        content = db_posts[post_id]["content"]

        # 2. summarize_post 함수 호출
        summary = summarize_post(title, content)
    # 3. 결과 반환
    return JSONResponse(
        content={
            "status": "Summary Created Successfully",
            "message": "요약 생성 완료",
            "data": summary,
        },
        status_code=201,
    )


# 게시글 요약용 함수
def summarize_post(title: str, content: str) -> str:
    # AI 클라이언트 객체 생성
    client = genai.Client()

    client.agents

    # 1. 프롬프트 구성
    prompt = f"다음 게시글을 한국어로 딱 한문장으로 간결하게 정리해줘. 제목 : {title}, 본문: {content}"

    # 2. Gemini 호출
    # 모델 예시
    response = client.models.generate_content(model="gemini-3.5-flash", contents=prompt)
    # 3. 응답 텍스트 반환
    return response.text
