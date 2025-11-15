import json, os, time

LOG_DIR = "data"
LOG_PATH = os.path.join(LOG_DIR, "usage_log.jsonl")
os.makedirs(LOG_DIR, exist_ok=True)

def log_event(event_type: str, mode: str, gesture: str | None = None, extra: dict | None = None, user: str | None = None):
    entry = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event_type,
        "mode": mode,
        "gesture": gesture,
        "user": user,
    }
    if extra:
        entry.update(extra)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
