import os
from dataclasses import dataclass


@dataclass
class ReportConfig:
    bot_token: str
    report_chat_id: str
    events_file: str


def load_report_config() -> ReportConfig:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise ValueError("BOT_TOKEN is empty")

    return ReportConfig(
        bot_token=token,
        report_chat_id=os.getenv("REPORT_CHAT_ID", "").strip(),
        events_file=os.getenv("EVENTS_FILE", "report_events.jsonl").strip(),
    )
