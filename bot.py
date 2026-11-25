
import os
import asyncio
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

app = Flask(__name__)

@app.route("/")
def home():
    return "MATRIX TOP UP BOT is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💎 Free Fire", callback_data="ff")],
        [InlineKeyboardButton("🎮 PUBG", callback_data="pubg")],
        [InlineKeyboardButton("⚽ DLS", callback_data="dls")],
        [InlineKeyboardButton("📢 Channel", url="https://t.me/your_channel")],
        [InlineKeyboardButton("👤 Support", url="https://t.me/your_username")]
    ]

    await update.message.reply_text(
        "👋 Welcome to MATRIX TOP UP BOT!\n\n"
        "💎 Select a service below:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    names = {
        "ff": "Free Fire",
        "pubg": "PUBG",
        "dls": "DLS"
    }

    await query.message.reply_text(
        f"You selected {names[query.data]}!\n"
        "Please contact our support for assistance."
    )

async def main():
    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CallbackQueryHandler(buttons))

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()
    await asyncio.Event().wait()

def run_server():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    asyncio.run(main())
