import json
from pathlib import Path

POST_FILE = Path("data/posts.json")
USED_FILE = Path("data/used_ids.json")

def get_next_post():
    # Загружаем список постов
    with open(POST_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    # Загружаем использованные посты (с защитой от пустого файла)
    used = set()
    if USED_FILE.exists():
        if USED_FILE.stat().st_size > 0:  # файл не пустой
            try:
                with open(USED_FILE, "r", encoding="utf-8") as f:
                    used = set(json.load(f))
            except json.JSONDecodeError:
                used = set()  # если файл битый — начинаем с пустого множества
        else:
            used = set()

    # Находим следующий пост
    for idx, post in enumerate(posts):
        if idx not in used:
            used.add(idx)
            with open(USED_FILE, "w", encoding="utf-8") as f:
                json.dump(list(used), f)
            return post

    return None
