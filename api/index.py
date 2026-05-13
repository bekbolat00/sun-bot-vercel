import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from flask import Flask, request, abort

BOT_TOKEN = os.environ.get("BOT_TOKEN", "ВСТАВЬ_СЮДА_ТОКЕН_БОТА")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "ВСТАВЬ_СЮДА_ЦИФРЫ_ID_САНЫ"))
WEB_APP_URL = "https://bekbolat00.github.io/sun-app/"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=["start"])
def handle_start(message):
    user = message.from_user
    first_name = user.first_name or ""
    username = f"@{user.username}" if user.username else "нет ника"
    user_id = user.id

    admin_text = (
        f"🚨 *Новый запуск бота!*\n\n"
        f"Имя: {first_name}\n"
        f"Ник: {username}\n"
        f"ID для таблицы: `{user_id}`\n\n"
        f"_(Нажми на цифры ID, чтобы скопировать)_"
    )

    try:
        bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
    except Exception:
        pass

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            "⚡️ Открыть SUN App",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )
    )

    bot.send_message(
        user_id,
        "Добро пожаловать в SUN! Твоя база знаний готова к работе 👇",
        reply_markup=keyboard
    )


@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get("content-type") != "application/json":
        abort(403)
    update = telebot.types.Update.de_json(request.get_data(as_text=True))
    bot.process_new_updates([update])
    return "ok", 200


@app.route("/", methods=["GET"])
def index():
    return "SUN Bot is running.", 200
