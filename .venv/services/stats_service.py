import json
from pathlib import Path
from datetime import datetime

FILE = Path("data/analytics.json")
FILE.parent.mkdir(exist_ok=True)

def log_post(title, message_id, date):
    if FILE.exists():
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append({
        "title": title,
        "message_id": message_id,
        "date": date,
        "views": 0
    })

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_post_views(message_id, views):
    if not FILE.exists():
        return

    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for post in data:
        if post["message_id"] == message_id:
            post["views"] = views

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_monthly_stats():
    if not FILE.exists():
        return []

    from datetime import datetime
    now = datetime.now()
    month = now.month
    year = now.year

    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [p for p in data if datetime.fromisoformat(p["date"]).month == month and datetime.fromisoformat(p["date"]).year == year]
