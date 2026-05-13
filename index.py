import os
import telebot
from flask import Flask, request

# 1. Читаем ключи из Vercel безопасно
TOKEN = os.environ.get('BOT_TOKEN', 'ТОКЕН_НЕ_НАЙДЕН')
ADMIN_ID = os.environ.get('ADMIN_ID', 'ID_НЕ_НАЙДЕН')
WEB_APP_URL = 'https://bekbolat00.github.io/sun-app/'

print(f"СТАРТ СИСТЕМЫ. Токен найден: {TOKEN != 'ТОКЕН_НЕ_НАЙДЕН'}. ID Админа: {ADMIN_ID}")

# Обязательно threaded=False для Vercel
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("--- ПОЛУЧЕНА КОМАНДА /START ---")
    user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    username_str = f"@{username}" if username else "скрыт"
    
    # Отправка уведомления Сане
    try:
        print(f"Пытаюсь отправить Сане на ID: {ADMIN_ID}...")
        admin_text = f"🚨 *Новый запуск бота!*\n\nИмя: {name}\nНик: {username_str}\nID: `{user_id}`"
        bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode='Markdown')
        print("УСПЕХ: Сана получила сообщение!")
    except Exception as e:
        print(f"ОШИБКА (Сана): {e}")
        
    # Ответ самому пользователю (тебе)
    try:
        print(f"Пытаюсь ответить юзеру {user_id}...")
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("⚡️ Открыть SUN App", web_app=telebot.types.WebAppInfo(url=WEB_APP_URL))
        markup.add(btn)
        bot.send_message(message.chat.id, "Добро пожаловать в SUN! Твоя база знаний готова к работе 👇", reply_markup=markup)
        print("УСПЕХ: Юзер получил кнопку!")
    except Exception as e:
        print(f"ОШИБКА (Юзер): {e}")

@app.route('/', methods=['POST'])
def webhook():
    print(">>> Телеграм стучится в Vercel!")
    try:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА ВЕБХУКА: {e}")
        return 'Error', 500