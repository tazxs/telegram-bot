from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from config import ADMIN_ID, CHANNEL_ID
from services.post_service import get_next_post
import random
import os

router = Router()

# === Папка с изображениями ===
IMAGE_FOLDER = "media/images"
DEFAULT_IMAGES = [
    os.path.join(IMAGE_FOLDER, name) for name in os.listdir(IMAGE_FOLDER)
    if name.lower().endswith((".jpg", ".png", ".jpeg", ".webp"))
]

# === Переменная для запоминания последней картинки ===
last_image_path = None

def get_post_image(post: dict) -> FSInputFile:
    """
    Возвращает FSInputFile:
    - если указано post['media'] и файл существует — берёт его;
    - иначе — случайную картинку, не равную последней.
    """
    global last_image_path
    media_path = post.get("media")

    if media_path and os.path.exists(media_path):
        last_image_path = media_path
        return FSInputFile(media_path)

    # Исключаем повторение последней картинки
    available_images = [img for img in DEFAULT_IMAGES if img != last_image_path]
    if not available_images:
        available_images = DEFAULT_IMAGES  # если вариантов мало — не исключаем

    selected = random.choice(available_images)
    last_image_path = selected
    return FSInputFile(selected)

@router.message(Command("post_now"))
async def manual_post(message: Message, bot: Bot):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Нет доступа")
        return

    post = get_next_post()
    if not post:
        await message.answer("❗ Постов больше нет")
        return

    caption = f"<b>{post['title']}</b>\n\n{post['tag']}\n\n{post['content']}"
    photo = get_post_image(post)

    await bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption=caption, parse_mode="HTML")
    await message.answer("✅ Пост отправлен")
