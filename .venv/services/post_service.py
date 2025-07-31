import json
from pathlib import Path

POST_FILE = Path("data/posts.json")
USED_FILE = Path("data/used_ids.json")

def get_next_post():
    with open(POST_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    if USED_FILE.exists():
        with open(USED_FILE, "r", encoding="utf-8") as f:
            used = set(json.load(f))
    else:
        used = set()

    for idx, post in enumerate(posts):
        if idx not in used:
            used.add(idx)
            with open(USED_FILE, "w", encoding="utf-8") as f:
                json.dump(list(used), f)
            return post
    return None
