import os
from dataclasses import dataclass
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from dotenv import load_dotenv


@dataclass
class ReportConfig:
    bot_token: str
    database_url: str
    private_chat_id: str
    auto_report_hours: int


def _add_sslmode_if_needed(database_url: str) -> str:
    parsed = urlparse(database_url)
    if not parsed.scheme or not parsed.netloc:
        return database_url
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if "sslmode" not in query:
        query["sslmode"] = "require"
        parsed = parsed._replace(query=urlencode(query))
    return urlunparse(parsed)


def load_report_config() -> ReportConfig:
    load_dotenv()
    token = os.getenv("BOT_TOKEN", "").strip()
    db_url = os.getenv("DATABASE_URL", "").strip()
    if not token:
        raise ValueError("BOT_TOKEN is empty")
    if not db_url:
        raise ValueError("DATABASE_URL is empty")
    return ReportConfig(
        bot_token=token,
        database_url=_add_sslmode_if_needed(db_url),
        private_chat_id=os.getenv("PRIVATE_CHAT_ID", "").strip(),
        auto_report_hours=int(os.getenv("AUTO_REPORT_HOURS", "24").strip()),
    )
