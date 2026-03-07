import json
from datetime import datetime
from pathlib import Path


def add_event(file_path: str, text: str):
    path = Path(file_path)
    item = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def read_events(file_path: str):
    path = Path(file_path)
    if not path.exists():
        return []
    items = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except Exception:
                continue
    return items


def get_last(file_path: str, limit: int = 10):
    return list(reversed(read_events(file_path)))[:limit]


def get_today(file_path: str):
    today = datetime.now().strftime("%Y-%m-%d")
    return [e for e in read_events(file_path) if str(e.get("time", "")).startswith(today)]


def get_stats(file_path: str):
    events = read_events(file_path)
    return {
        "total": len(events),
        "new": sum(1 for e in events if "🆕 Новая заявка" in e.get("text", "")),
        "paid": sum(1 for e in events if "💰 Клиент отметил оплату" in e.get("text", "")),
        "wallet": sum(1 for e in events if "🚨 Wallet заявка" in e.get("text", "")),
        "qr": sum(1 for e in events if "📷 Запрос QR-кода" in e.get("text", "")),
    }
