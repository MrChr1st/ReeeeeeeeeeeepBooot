from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from report_storage import add_event, get_last, get_stats, get_today

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "📊 Repoorrttt bot online\n\n"
        "Команды:\n"
        "/help\n"
        "/last\n"
        "/today\n"
        "/stats"
    )


@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "Команды:\n"
        "/last - последние события\n"
        "/today - события за сегодня\n"
        "/stats - статистика"
    )


@router.message(Command("last"))
async def last_cmd(message: Message, config):
    items = get_last(config.events_file, 10)
    if not items:
        await message.answer("Событий пока нет")
        return

    text = "📚 Последние события\n\n" + "\n\n".join(
        f"{item['time']}\n{item['text']}" for item in items
    )
    await message.answer(text[:4096])


@router.message(Command("today"))
async def today_cmd(message: Message, config):
    items = get_today(config.events_file)
    if not items:
        await message.answer("Сегодня событий пока нет")
        return

    text = "📅 События за сегодня\n\n" + "\n\n".join(
        f"{item['time']}\n{item['text']}" for item in items[-20:]
    )
    await message.answer(text[:4096])


@router.message(Command("stats"))
async def stats_cmd(message: Message, config):
    stats = get_stats(config.events_file)
    await message.answer(
        "📊 Статистика\n\n"
        f"Всего событий: {stats['total']}\n"
        f"Новых заявок: {stats['new']}\n"
        f"Оплачено: {stats['paid']}\n"
        f"Wallet: {stats['wallet']}\n"
        f"QR запросы: {stats['qr']}"
    )


@router.message(F.chat.type.in_({"group", "supergroup"}))
async def log_group_message(message: Message, config):
    if message.text:
        add_event(config.events_file, message.text)
