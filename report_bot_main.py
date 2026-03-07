import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from report_bot_config import load_report_config
from report_handlers import router


async def main():
    logging.basicConfig(level=logging.INFO)

    config = load_report_config()
    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp["config"] = config
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
