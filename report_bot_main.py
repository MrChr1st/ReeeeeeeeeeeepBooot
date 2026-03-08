import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile

from report_bot_config import load_report_config
from report_handlers import router
from reportbot_shared import generate_excel_report_24h
from shared_storage import SharedStorage


STATE_FILE = "reportbot_last_sent.txt"


def _read_last_sent() -> str:
    p = Path(STATE_FILE)
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def _write_last_sent(value: str):
    Path(STATE_FILE).write_text(value, encoding="utf-8")


def _stats_text(storage) -> str:
    stats = storage.get_stats_24h()
    totals = "\n".join(f"• {cur}: {amt:.8f}" for cur, amt in sorted(stats["totals"].items())) or "—"
    return (
        "📊 Отчет за 24ч\n\n"
        f"👥 Открыли обмен: {stats['opened']}\n"
        f"🧾 Создано заявок: {stats['new_requests']}\n"
        f"💰 Оплачено: {stats['paid']}\n"
        f"⏳ Не оплачено: {stats['unpaid']}\n"
        f"📷 QR запросы: {stats['qr']}\n"
        f"🚨 Срочных wallet: {stats['wallet']}\n\n"
        "💱 Оборот:\n"
        f"{totals}"
    )


async def auto_sender(bot: Bot, storage: SharedStorage, private_chat_id: str, hours: int):
    while True:
        try:
            if private_chat_id:
                last = _read_last_sent()
                now = datetime.now()
                should_send = False
                if not last:
                    should_send = True
                else:
                    try:
                        dt = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
                        should_send = now - dt >= timedelta(hours=max(hours, 1))
                    except Exception:
                        should_send = True
                if should_send:
                    file_path = generate_excel_report_24h(storage)
                    document = FSInputFile(file_path, filename=f"report_24h_{now.strftime('%Y%m%d_%H%M%S')}.xlsx")
                    await bot.send_document(chat_id=private_chat_id, document=document, caption="📊 Автоотчёт Excel за 24 часа")
                    await bot.send_message(chat_id=private_chat_id, text=_stats_text(storage))
                    _write_last_sent(now.strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            logging.exception(f"[reportbot auto_sender] failed: {e}")
        await asyncio.sleep(300)


async def main():
    logging.basicConfig(level=logging.INFO)
    config = load_report_config()
    storage = SharedStorage(config.database_url)
    storage.init()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp["storage"] = storage
    dp.include_router(router)

    asyncio.create_task(auto_sender(bot, storage, config.private_chat_id, config.auto_report_hours))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
