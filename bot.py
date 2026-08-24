import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo
from fastapi import FastAPI
import uvicorn

TOKEN = "8765127226:AAFAZzn9V7TVwsgWj-ihgzyEKGH_gIHHv1k"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render port talabini bajarish uchun kichik veb-server
app = FastAPI()


@app.get("/")
def health_check():
  return {"status": "Bot ishlayapti!"}


@dp.message(Command("start"))
async def cmd_start(message: Message):
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

  # Render beradigan PORT'ni olib serverni va botni birga yurgizamiz
  port = int(os.getenv("PORT", 10000))
  config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
  server = uvicorn.Server(config)

  print("Bot va Veb-server ishga tushdi...")
  await asyncio.gather(server.serve(), dp.start_polling(bot))


if __name__ == "__main__":
  asyncio.run(main())
