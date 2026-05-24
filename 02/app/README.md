# 2주차 Weekly Challenge
## 과제 목표
- 1: HTTP 내용정리
- 2: 커뮤니티 게시판 구현
  - [x] 2-1: 게시글 CRUD, 댓글 CRUD 기능 추가 
  - [x] 2-2: LLM API 연동하여 게시글 요약 기능 추가
  - [x] 2-3: 데이터베이스 연동
  - [x] 2-4: 구조 개선 (디자인 패턴으로 리팩토링)
  - [ ] 2-5(선택): HTML, CSS, javascript나 Streamlit을 이용하여 프론트엔드 구현
## 프로젝트 개요
### 프로젝트 구조
 ```
 02
 ├── app
 │   ├── main.py
 │   ├── models.py       # 데이터 모델
 │   └── routers
 │   │   ├── __init__.py
 │   │   ├── post.py     # 게시글 라우터
 │   │   ├── comment.py  # 댓글 라우터
 │   │   └── summary.py  # 로컬 LLM 요약 라우터
 │   ├── pyproject.toml
 │   └── README.md
 ├── 02-1
 │   └── HTTP_Summary.md # HTTP 내용 정리

```
### 주요 기능


### API Spec

- Default
  |Method|Endpoint|Description|
  |---|---|---|
  |GET|/|root 페이지 조회|
- Post
  |Method|Endpoint|Description|
  |---|---|---|
  |GET|/posts|전체 게시글 조회|
  |GET|/posts/{post_id}|특정 게시글 조회|
  |POST|/posts|게시글 생성|
  |PATCH|/posts/{post_id}|특정 게시글 수정|
  |DELETE|/posts/{post_id}|특정 게시글 삭제|
- Comment
  |Method|Endpoint|Description|
  |------|---|---|
  |GET|/posts/{post_id}/comments|특정 게시글의 전체 댓글 조회|
  |GET|/posts/{post_id}/comments/{comment_id}|특정 댓글 조회|
  |POST|/posts/{post_id}/comments|댓글 생성|
  |PATCH|/posts/{post_id}/comments/{comment_id}|특정 댓글 수정|
  |DELETE|/posts/{post_id}/comments/{comment_id}|특정 댓글 삭제|
- Summary
  |Method|Endpoint|Description|
  |------|---|---|
  |POST|/posts/{post_id}/summary|AI로 게시글 요약 생성|



### 데이터베이스
이 프로젝트에서는 `sqlite`를 사용하였다. 이유는 별도의 설정이 필요없이 간단하게 설치가 가능하고 모든 데이터를 파일 하나로 관리할 수 있기 때문에, DB와 API를 연동하는게 목적이었던 이 프로젝트에 적합하다고 느꼈다. 


## 실행방법

### 가상환경
`python3 -m venv .venv`  

`source .venv/bin/activate`
### 라이브러리 설치
`uv add "fastapi[standard]`  

`uv add sqlmodel`  

`uv add ollama`  

### 실행
`fastapi dev`
### 종료
`deactivate`



## 회고

이번주 과제로 FastAPI를 사용해 간단한 커뮤니티 게시판 백엔드를 구현했다. 공식문서로 공부하면서 느끼는 건데 생각보다 매우 친절하게 설명되어 이해하기 편했지만 이를 프로젝트에 적용시키는데 조금 어려움이 있었다. 그리고 처음에 AI를 이용한 요약 기능을 추가할 떄 `Ollama`(로컬 llm)이 아니라 `Google genai`를 먼저 적용했었다. 하지만 Github에 `push`하는 과정에서 발급받았던 `GEMINI_API_KEY`가 유출되는 일이 있었다. 늦지 않게 발견해 Commit History도 덮어씌우고 키도 다시 발급받았지만 이를 통해 `.gitignore` 설정의 중요성을 다시 알게되었다. 이번에 과제를 하면서 사용했던 `sqlmodel`, `ollama`도 아직 제대로 이해하지 못하고 적용만 시킨 것 같아서 공식문서를 토대로 더 공부해야할 것 같다. 그리고 마지막에 DB 연동을 하면서 `main.py`에서 여러개의 파일로 나누며 구조개선을 진행했는데 생각보다 오래걸렸던 것 같다. 큰 프로젝트일수록 구조개선에 어려움이 있을테니 항상 좋은 구조에 대해 생각하고 많은 연습이 필요할 것 같다.

### 개선방향
- `models.py`에서 구현만한 response모델들을 적용
- 좋아요나 조회수 같은 속성들 추가
- Streamlit을 이용한 프론트엔드 구현