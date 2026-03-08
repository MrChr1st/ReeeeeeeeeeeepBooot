
from report_storage import get_financial_report, get_opened_today

async def send_daily_fin_summary(bot, config):
    report = get_financial_report(config.events_file)
    opened = get_opened_today(config.events_file)

    text = (
        "📊 Отчет за 24ч\n\n"
        f"👥 Открыли обмен: {len(opened)}\n"
        f"🧾 Создано заявок: {report['new_requests']}\n"
        f"💰 Оплачено: {report['paid_requests']}\n"
        f"⏳ Не оплачено: {max(report['new_requests']-report['paid_requests'],0)}"
    )

    if config.private_chat_id:
        await bot.send_message(config.private_chat_id, text)
