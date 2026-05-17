# 📝 todo — 간단한 할일 관리 CLI

JSON 파일로 관리되는 간단한 할일 관리 CLI.

---

## 실행 환경

- Python 3.8+
- 외부 라이브러리 없음 (표준 라이브러리 `argparse`, `json`, `os` 만 사용)

---

## 명령어 정리

| 명령어 | 인자 | 설명 |
|------|----|----|
| `add` | `content` (필수) | 할일 내용 추가 |
| `list` | — | 전체 할일 목록 출력 |
| `done` | `id` (필수, 정수) | 해당 id 할일을 완료로 표시 |
| `remove` | `id` (필수, 정수) | 해당 id 할일 삭제 |

---

## 사용법

### 할일 추가
```bash
python3 todo.py add "1주차 강의 정리"
python3 todo.py add "Git & Github 공부"
```

### 목록 보기
```bash
python3 todo.py list
```

### 완료 처리
```bash
python3 todo.py done 1
```

### 할일 삭제
```bash
python3 todo.py remove 1
```

### 도움말
```bash
python3 todo.py --help
python3 todo.py add --help
```

---

