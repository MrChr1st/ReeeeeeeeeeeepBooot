from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, KeyboardButton, Message, ReplyKeyboardMarkup

from reportbot_shared import generate_excel_report_24h

router = Router()


def bottom_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="💵 Фин. отчет")],
            [KeyboardButton(text="👤 Кто открыл"), KeyboardButton(text="📄 Excel 24ч")],
        ],
        resize_keyboard=True,
    )


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


@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("📊 Repoorrttt bot online", reply_markup=bottom_menu_kb())


@router.message(Command("stats"))
@router.message(F.text == "📊 Статистика")
async def stats_cmd(message: Message, storage):
    await message.answer(_stats_text(storage), reply_markup=bottom_menu_kb())


@router.message(Command("opened"))
@router.message(F.text == "👤 Кто открыл")
async def opened_cmd(message: Message, storage):
    rows = storage.get_opened_rows_24h()
    if not rows:
        await message.answer("За последние 24 часа никто не открывал обмен", reply_markup=bottom_menu_kb())
        return
    body = "\n\n".join(
        f"{row['created_at']}\n@{row['username']}" if row.get("username") else f"{row['created_at']}\nid={row['user_id']}"
        for row in rows[-50:]
    )
    await message.answer(("👤 Кто открывал обмен за 24 часа\n\n" + body)[:4096], reply_markup=bottom_menu_kb())


@router.message(Command("finreport"))
@router.message(F.text == "💵 Фин. отчет")
async def finreport_cmd(message: Message, storage):
    await message.answer(_stats_text(storage), reply_markup=bottom_menu_kb())


@router.message(Command("xlsx24"))
@router.message(F.text == "📄 Excel 24ч")
async def xlsx24_cmd(message: Message, storage):
    file_path = generate_excel_report_24h(storage)
    document = FSInputFile(file_path, filename=f"report_24h_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    await message.answer_document(document, caption="📊 Excel отчёт за последние 24 часа", reply_markup=bottom_menu_kb())
