import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile

from report_bot_config import load_report_config
from report_handlers import make_excel_report, router


async def auto_excel_sender(bot: Bot, config):
    while True:
        try:
            hours = max(int(config.auto_report_hours), 1)
            await asyncio.sleep(hours * 60 * 60)

            if not config.private_chat_id:
                logging.warning("[auto_excel_sender] PRIVATE_CHAT_ID is empty")
                continue

            file_path = make_excel_report(config)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            document = FSInputFile(file_path, filename=f"report_24h_{timestamp}.xlsx")

            await bot.send_document(
                chat_id=config.private_chat_id,
                document=document,
                caption="📊 Автоотчёт за последние 24 часа",
            )
            logging.info("[auto_excel_sender] daily report sent")
        except Exception as e:
            logging.exception(f"[auto_excel_sender] failed: {e}")


async def main():
    logging.basicConfig(level=logging.INFO)

    config = load_report_config()
    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp["config"] = config
    dp.include_router(router)

    asyncio.create_task(auto_excel_sender(bot, config))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
