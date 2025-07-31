from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import ADMIN_ID
from services.stats_service import get_monthly_stats

router = Router()

@router.message(Command("stats"))
async def show_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    stats = get_monthly_stats()
    total = len(stats)
    top = sorted(stats, key=lambda x: x["views"], reverse=True)[:3]

    text = f"<b>📊 Статистика за текущий месяц</b>\n"
    text += f"Всего постов: <b>{total}</b>\n\n"

    if not top:
        text += "Нет постов с просмотром."
    else:
        text += "🏆 <b>Топ 3 по просмотрам:</b>\n"
        for i, p in enumerate(top, 1):
            text += f"{i}) {p['title']} — {p['views']} 👁️\n"

    await message.answer(text)
