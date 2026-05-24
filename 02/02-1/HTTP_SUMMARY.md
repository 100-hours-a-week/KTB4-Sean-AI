# HTTP Summary

## HTTP란?

### 기술적 정의
**HyperText Transfer Protocol** — TCP 위에서 동작하는, 클라이언트와 서버 간 메시지 교환 프로토콜.

- **Hyper**Text: plain text(HTML/CSS/JS)뿐 아니라 이미지·오디오·링크 등 멀티미디어까지 연결해 다루는 텍스트.
- 메시지 종류는 두 가지: **Request**(요청)와 **Response**(응답).
- 대표적인 클라이언트는 **브라우저**.

### 나만의 정리
클라이언트와 서버간에 일반적인 텍스트만 아니라 하이퍼텍스트를 주고 받기 위한 통신 규약.

## HTTP 요청 (Request)

- 클라이언트가 서버에 보내는 메시지. "무엇을, 어떻게, 어떤 데이터와 함께 처리해 달라"를 담는다.
- 헤더와 바디 사이에는 공백으로 구분

### 구성요소

| 구성 | 설명 |
|---|---|
| **Start line** | 메서드 + URL + HTTP 버전 (예: `GET /posts/3 HTTP/1.1`) |
| **Headers** | 메타 정보 (Host, Content-Type, Authorization 등) |
| **Body** | 실제 데이터 (POST/PUT/PATCH에서 주로 사용, GET은 보통 없음) |



## HTTP 응답(Response)

서버가 클라이언트에 돌려보내는 메시지. Request와 마찬가지로 세가지 구성요소가 있다.

| 구성 | 설명 |
|---|---|
| **Status line** | HTTP 버전 + 상태 코드 + 상태 메시지 (예: `HTTP/1.1 200 OK`) |
| **Headers** | 응답 메타 정보 (Content-Type, Content-Length 등) |
| **Body** | 응답 데이터 (JSON, HTML, 이미지 등) |


## HTTP Method

> HTTP defines a set of request methods to indicate the purpose of the request and what is expected if the request is successful. (MDN 공식문서

클라이언트가 서버가 수행해야 할 요청을 보내는 방법

| Method | 용도 | Body | CRUD |
|---|---|---|---|
| **GET** | 자원 조회 | 없음 (매개변수는 경로 변수 / 쿼리 스트링) | Read |
| **POST** | 자원 생성 | 있음 | Create |
| **PUT** | 자원 **전체** 수정 | 있음 | Update |
| **PATCH** | 자원 **부분** 수정 | 있음 | Update |
| **DELETE** | 자원 삭제 | (선택) | Delete |


## HTTP 상태 코드(Status Code)

- 응답의 결과를 분류하는 3자리 숫자.
- **판단의 주체는 서버**이며, 코드 자체가 판단을 하는 게 아니다.

| 분류 | 의미 | 예시 |
|---|---|---|
| **1xx** | 정보 메시지 | 100 Continue |
| **2xx** | 성공 | 200 OK, 201 Created, 204 No Content |
| **3xx** | 리다이렉션 | 301 Moved Permanently, 304 Not Modified |
| **4xx** | 클라이언트 오류 | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| **5xx** | 서버 오류 | 500 Internal Server Error, 503 Service Unavailable |

> 면접에 자주 나오는 주제로 주요 코드 암기 필수

## HTTP URL

### 구조

```
scheme://domain:port/path?query
```

| 구성 | 설명 | 예시 |
|---|---|---|
| **scheme** | 프로토콜 | `http`, `https`, `ftp`...|
| **domain** | 호스트 주소 | `example.com`, `localhost` |
| **port** | 동일 IP 안에서 서비스를 구분하는 번호 | `80`(HTTP 기본), `443`(HTTPS 기본) → 생략 가능 |
| **path** | 서버 안에서의 세분화된 주소 | `/posts/3` |
| **query** | `?` 뒤에 붙는 추가 매개변수 | `?page=2&sort=desc` |

### 경로 변수 vs 쿼리 스트링

| 구분 | 형식 | 용도 |
|---|---|---|
| **경로 변수 (Path Parameter)** | `/posts/3` — URL 경로 자체에 박힌 값 | 특정 자원을 **식별**할 때 |
| **쿼리 스트링 (Query String)** | `?key=value&key2=value2` (`&`로 연결) | **필터링·정렬·페이징** 등 부가 조건 |



## REST API

**RE**presentational **S**tate **T**ransfer — 자원을 **URI**로 식별하고, **HTTP 메서드**로 동작을 표현하며, **JSON 등의 형식**으로 자원의 상태를 주고받는 아키텍처 스타일.

> 면접 단골 정의: **"이름(URI 패턴) + 교환 방식(HTTP 메서드) + 메시지 형식(JSON)"**

### 왜 쓰는가
- HTTP의 표준을 그대로 활용 → 별도 학습 비용이 작고 캐싱·확장에 유리.
- URI만 봐도 어떤 자원인지, 메서드만 봐도 어떤 동작인지 직관적으로 드러남 → **협업과 문서화에 강함**.
- 클라이언트-서버 결합도가 낮아 모바일·웹·서버 간 통신에 두루 적합.

### 7가지 규칙
1. URI는 **자원**을 표현한다 (명사 사용, 동사 X)
2. 자원의 **행위**는 HTTP 메서드로 표현 (CRUD ↔ POST/GET/PUT·PATCH/DELETE)
3. `/`는 **계층 관계**를 표현
4. URI는 **소문자** 사용
5. 단어 구분은 언더스코어(`_`) 대신 **하이픈(`-`)**
6. **확장자**(`.png`, `.txt`)는 URI에 쓰지 않음
7. URI 끝에 **`/`를 붙이지 않음**

### 예시

| 동작 | Method | URI |
|---|---|---|
| 게시글 목록 조회 | GET | `/posts` |
| 특정 게시글 조회 | GET | `/posts/3` |
| 게시글 작성 | POST | `/posts` |
| 게시글 전체 수정 | PUT | `/posts/3` |
| 게시글 부분 수정 | PATCH | `/posts/3` |
| 게시글 삭제 | DELETE | `/posts/3` |

> **주의**: REST는 *de facto standard*일 뿐, 사람마다·회사마다 해석이 다르다. 절대적인 정답은 없다.




