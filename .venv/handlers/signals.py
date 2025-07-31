from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from config import CHANNEL_ID, ADMIN_ID
from pathlib import Path

router = Router()

@router.message(Command("signal"))
async def send_signal(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Нет доступа")
        return

    try:
        args = message.text.split()[1:]
        coin = args[0].upper()
        entry_type = args[1].lower()
        entry_price = args[2]
        stop_index = args.index("стоп")
        take_index = args.index("тейк")
        stop = args[stop_index + 1]
        takes = args[take_index + 1:]
        take_str = " / ".join(takes)

        text = (
            f"📢 <b>SIGNAL: {coin}</b>\n"
            f"💠 Тип входа: <i>{entry_type}</i> по <b>{entry_price}</b>\n"
            f"❌ Стоп: {stop}\n"
            f"🎯 Тейки: {take_str}"
        )

        if message.photo:
            file_id = message.photo[-1].file_id
            await message.bot.send_photo(CHANNEL_ID, file_id, caption=text)
        else:
            photo = None
            base_dir = Path("media/signals")
            if "лонг" in entry_type:
                photo = base_dir / "long.jpg"
            elif "шорт" in entry_type:
                photo = base_dir / "short.jpg"

            if photo and photo.exists():
                await message.bot.send_photo(CHANNEL_ID, FSInputFile(photo), caption=text)
            else:
                await message.bot.send_message(CHANNEL_ID, text)

        await message.answer("✅ Сигнал отправлен")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}\n\nФормат:\n/signal BTC лонг 32000 стоп 31000 тейк 35000 36000")
