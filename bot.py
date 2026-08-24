import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

# Bot tokeningizni shu yerga yozasiz
TOKEN = "8765127226:AAFAZzn9V7TVwsgWj-ihgzyEKGH_gIHHv1k"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Saytingiz manzili (Render'dagi link)
    web_app_url = "https://flash-typing.onrender.com"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⚡ ProTyping Studio'ni ochish",
                    web_app=WebAppInfo(url=web_app_url),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏆 Reytingni ko'rish", callback_data="leaderboard"
                )
            ],
        ]
    )

    await message.answer(
        f"Assalomu alaykum, <b>{message.from_user.full_name}</b>! 👋\n\n"
        "<b>ProTyping Studio</b> – professional tez yozish trenajyoriga xush kelibsiz.\n"
        "Mashq qilish uchun quyidagi tugmani bosing:",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
