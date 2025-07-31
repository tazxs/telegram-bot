import pytz
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from config import CHANNEL_ID, TIMEZONE
from services.post_service import get_next_post
from aiogram import Bot
from services.stats_service import log_post, update_post_views
from services.stats_service import get_monthly_stats

times = ["08:00", "11:00", "14:00", "17:00", "20:00"]  # 5 постов в день (UTC-4)

# ⬆️ Импорты
from services.stats_service import get_monthly_stats
from config import CHANNEL_ID
from aiogram import Bot

async def post_monthly_report(bot: Bot):
    stats = get_monthly_stats()
    top = sorted(stats, key=lambda x: x["views"], reverse=True)[:3]

    if not top:
        return

    text = "<b>📈 Месячная аналитика</b>\n\n"
    text += "🏆 <b>Топ 3 поста:</b>\n"
    for i, p in enumerate(top, 1):
        text += f"{i}) {p['title']} — {p['views']} 👁️\n"

    await bot.send_message(CHANNEL_ID, text)

# ✅ Теперь определена ДО вызова
def setup_scheduler(bot: Bot):
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    import pytz
    from config import TIMEZONE
    from services.post_service import get_next_post
    from datetime import datetime
    import asyncio

    scheduler = AsyncIOScheduler(timezone=pytz.timezone(TIMEZONE))

    times = ["08:00", "11:00", "14:00", "17:00", "20:00"]
    for t in times:
        hour, minute = map(int, t.split(":"))
        scheduler.add_job(send_scheduled_post, CronTrigger(hour=hour, minute=minute), args=[bot])

    # ⬇️ Вот теперь можем вызвать!
    scheduler.add_job(post_monthly_report, CronTrigger(day=1, hour=9), args=[bot])
    scheduler.start()

async def send_scheduled_post(bot: Bot):
    from services.post_service import get_next_post
    from services.stats_service import log_post, update_post_views
    from config import CHANNEL_ID
    from datetime import datetime
    import asyncio

    post = get_next_post()
    if post:
        message = f"<b>{post['title']}</b>\n\n{post['tag']}\n\n{post['content']}"
        msg = None
        if post["media"]:
            msg = await bot.send_photo(CHANNEL_ID, photo=post["media"], caption=message)
        else:
            msg = await bot.send_message(CHANNEL_ID, text=message)

        if msg:
            log_post(post["title"], msg.message_id, datetime.utcnow().isoformat())
            await asyncio.sleep(5)
            views = await bot.get_message(CHANNEL_ID, msg.message_id)
            update_post_views(msg.message_id, views.views or 0)

