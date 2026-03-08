import os
from dataclasses import dataclass


@dataclass
class ReportConfig:
    bot_token: str
    database_url: str
    private_chat_id: str
    auto_report_hours: int


def load_report_config() -> ReportConfig:
    token = os.getenv("BOT_TOKEN", "").strip()
    db_url = os.getenv("DATABASE_URL", "").strip()
    if not token:
        raise ValueError("BOT_TOKEN is empty")
    if not db_url:
        raise ValueError("DATABASE_URL is empty")
    return ReportConfig(
        bot_token=token,
        database_url=db_url,
        private_chat_id=os.getenv("PRIVATE_CHAT_ID", "").strip(),
        auto_report_hours=int(os.getenv("AUTO_REPORT_HOURS", "24").strip()),
    )
