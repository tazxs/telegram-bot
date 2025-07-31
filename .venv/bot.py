import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from scheduler import setup_scheduler
from config import BOT_TOKEN
from handlers import admin, signals, stats  # Импорт всех хендлеров

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
dp.include_router(admin.router)
dp.include_router(signals.router)
dp.include_router(stats.router)

async def main():
    setup_scheduler(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
