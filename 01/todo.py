"""
todo.py — 아주 간단한 할일 관리 CLI

사용법:
  python3 todo.py add "할일 내용"
  python3 todo.py list
  python3 todo.py done 1
  python3 todo.py remove 1

json으로 데이터 저장
argparse 사용할 것
"""

import argparse
import json
import os

# 이 파이썬 파일과 같은 폴더에 tasks.json 을 저장
DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


# load tasks 함수 - json 파일로 데이터 불러오기
def load_tasks():
    # tasks.json 이 없으면 빈 리스트 반환
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# save task 함수 - json 파일에 데이터 쓰기
def save_tasks(tasks):
    # 리스트를 tasks.json 에 저장.
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)



# add task 함수 - 항목 추가, 인덱스 부여
def command_add(content):
    tasks = load_tasks()
    # 새 id 는 (지금까지 가장 큰 id + 1). 비어있으면 1부터.
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": new_id, "content": content, "done": False})
    save_tasks(tasks)
    print(f"추가됨: #{new_id} {content}")


# list 함수 - 모든 할일 내용 출력, 완료 항목은 [x]로 나타냄
def command_list():
    tasks = load_tasks()
    if not tasks:
        print("할일이 없습니다.")
        return
    print(f"=== 할일 목록 ===")
    for t in tasks:
        check = "[x]" if t["done"] else "[ ]"
        print(f"{check} #{t['id']} {t['content']}")

# done 함수 - 선택한 항목 완료 목록으로 만들기
def command_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"완료 처리: #{task_id} {t['content']}")
            return
    print(f"#{task_id} 를 찾을 수 없습니다.")


# remove 함수 - 선택한 항목 제거
def command_remove(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    # 선택한 id가 없으면 오류 반환
    if len(new_tasks) == len(tasks):
        print(f"#{task_id} 를 찾을 수 없습니다.")
        return
    save_tasks(new_tasks)
    print(f"삭제됨: #{task_id}")

def main():
    parser = argparse.ArgumentParser(description="간단한 할일 관리 CLI")
    subparsers = parser.add_subparsers(dest="command")

    # add
    p_add = subparsers.add_parser("add", help="할일 추가")
    p_add.add_argument("content", help="할일 내용")

    # list
    subparsers.add_parser("list", help="할일 목록 보기")

    # done
    p_done = subparsers.add_parser("done", help="할일을 완료로 표시")
    p_done.add_argument("id", type=int, help="할일 id")

    # remove
    p_remove = subparsers.add_parser("remove", help="할일 삭제")
    p_remove.add_argument("id", type=int, help="할일 id")

    args = parser.parse_args()

    # 명령어에 따라 함수 실행
    if args.command == "add":
        command_add(args.content)
    elif args.command == "list":
        command_list()
    elif args.command == "done":
        command_done(args.id)
    elif args.command == "remove":
        command_remove(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()