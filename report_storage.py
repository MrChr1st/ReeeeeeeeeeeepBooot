
import json
from datetime import datetime, timedelta
from pathlib import Path


def _read(file):
    path = Path(file)
    if not path.exists():
        return []
    items = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                items.append(json.loads(line))
            except Exception:
                pass
    return items


def add_event(file, text):
    item = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text,
    }
    with open(file, "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def get_last(file, limit=10):
    return _read(file)[-limit:]


def get_today(file):
    today = datetime.now().strftime("%Y-%m-%d")
    return [e for e in _read(file) if e["time"].startswith(today)]


def get_last_24h(file):
    now = datetime.now()
    res = []
    for e in _read(file):
        try:
            t = datetime.strptime(e["time"], "%Y-%m-%d %H:%M:%S")
            if now - t <= timedelta(hours=24):
                res.append(e)
        except Exception:
            pass
    return res


def build_opened_rows(events):
    rows = []
    for e in events:
        if "Открыл обмен" in e["text"] or "Exchange opened" in e["text"]:
            rows.append({
                "time": e["time"],
                "user": e["text"],
                "user_id": "",
                "profile": ""
            })
    return rows


def build_request_rows(events):
    rows = []
    for e in events:
        if "Новая заявка" in e["text"]:
            rows.append({
                "time": e["time"],
                "request_id": "",
                "user": e["text"],
                "user_id": "",
                "profile": "",
                "from_cur": "",
                "to_cur": "",
                "amount_from": "",
                "amount_to": "",
                "details": "",
                "payment": "",
                "status": "created",
                "paid_at": "",
            })
        if "Клиент отметил оплату" in e["text"]:
            rows.append({
                "time": e["time"],
                "request_id": "",
                "user": e["text"],
                "user_id": "",
                "profile": "",
                "from_cur": "",
                "to_cur": "",
                "amount_from": "",
                "amount_to": "",
                "details": "",
                "payment": "",
                "status": "paid",
                "paid_at": e["time"],
            })
    return rows


def get_stats(file):
    events = _read(file)
    return {
        "total": len(events),
        "new": sum("Новая заявка" in e["text"] for e in events),
        "paid": sum("отметил оплату" in e["text"] for e in events),
        "wallet": 0,
        "qr": sum("QR" in e["text"] for e in events),
        "opened": sum("обмен" in e["text"].lower() for e in events),
    }


def get_financial_report(file):
    events = _read(file)
    return {
        "new_requests": sum("Новая заявка" in e["text"] for e in events),
        "paid_requests": sum("отметил оплату" in e["text"] for e in events),
        "from_totals": {},
        "to_totals": {},
    }


def get_opened_today(file):
    today = datetime.now().strftime("%Y-%m-%d")
    return [e for e in _read(file) if e["time"].startswith(today) and "обмен" in e["text"].lower()]
