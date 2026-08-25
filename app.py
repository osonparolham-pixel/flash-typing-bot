import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = os.getenv("BOT_TOKEN", "8765127226:AAFAZzn9V7TVwsgWj-ihgzyEKGH_gIHHv1k")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://flash-typing.onrender.com")

bot = Bot(token=TOKEN)
dp = Dispatcher()

app = FastAPI()

# 1. /start komandasi
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⚡ ProTyping Studio'ni ochish", web_app=WebAppInfo(url=WEBAPP_URL))
        ],
        [
            InlineKeyboardButton(text="🏆 Reytingni ko'rish", callback_data="leaderboard_btn")
        ]
    ])
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}! ⚡ ProTyping Studio trenajyoriga xush kelibsiz.\n\nQuyidagi tugmalar orqali davom eting:",
        reply_markup=kb
    )

# 2. Reyting tugmasi
@dp.callback_query(lambda c: c.data == "leaderboard_btn")
async def process_leaderboard(callback: types.CallbackQuery):
    await callback.message.answer("🏆 Hozircha reyting jadvali bo'sh. Tez orada eng yaxshi natijalar shu yerda ko'rsatiladi! 🚀")
    await callback.answer()

# 3. Web App sahifasi
@app.get("/", response_class=HTMLResponse)
async def read_root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "ProTyping Studio ishga tushdi! index.html topilmadi."

# 4. Telegramdan keladigan xabarlarni qabul qilish (Webhook)
@app.post("/webhook")
async def webhook(request: Request):
    json_data = await request.json()
    update = types.Update.model_validate(json_data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"status": "ok"}

# 5. Render ishga tushganda Webhook'ni avtomatik sozlash
@app.on_event("startup")
async def on_startup():
    webhook_url = f"{WEBAPP_URL}/webhook"
    await bot.set_webhook(webhook_url)

@app.get("/ping")
async def ping():
    return {"status": "alive"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
