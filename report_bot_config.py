import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class ReportConfig:
    bot_token: str
    database_url: str
    private_chat_id: str
    auto_report_hours: int


def _load_env_file() -> None:
    base_dir = Path(__file__).resolve().parent
    load_dotenv(base_dir / ".env")
    load_dotenv()


def _ensure_sslmode_require(database_url: str) -> str:
    value = (database_url or "").strip()
    if not value:
        return value
    if "sslmode=" in value:
        return value
    parts = urlsplit(value)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["sslmode"] = "require"
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def load_report_config() -> ReportConfig:
    _load_env_file()
    token = os.getenv("BOT_TOKEN", "").strip()
    db_url = _ensure_sslmode_require(os.getenv("DATABASE_URL", "").strip())
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
