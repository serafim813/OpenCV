import json


def settings():
    with open("config.json", "r", encoding="utf-8") as f:
        return dict(json.loads(f.read()))


CFG = settings()

DB_URL = CFG.get("url", None)