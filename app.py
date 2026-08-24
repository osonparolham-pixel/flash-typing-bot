import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo
from fastapi import FastAPI
import uvicorn

# Bot tokeni
TOKEN = os.getenv("BOT_TOKEN", "8765127226:AAFAZzn9V7TVwsgWj-ihgzyEKGH_gIHHv1k")
bot = Bot(token=TOKEN)
dp = Dispatcher()

app = FastAPI()


@app.get("/")
def home():
  return {"status": "Server ishlamoqda!"}


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


# FastAPI ishga tushishi bilan bot polling ham birga yonadi
@app.on_event("startup")
async def startup_event():
  asyncio.create_task(dp.start_polling(bot))
  print("Telegram bot polling muvaffaqiyatli boshlandi!")


if __name__ == "__main__":
  port = int(os.getenv("PORT", 10000))
  uvicorn.run("app:app", host="0.0.0.0", port=port)
