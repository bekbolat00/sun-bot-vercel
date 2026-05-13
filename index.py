import os
import telebot
from flask import Flask, request

# Достаем ключи из Vercel Environment Variables
TOKEN = os.environ.get('BOT_TOKEN', '')
ADMIN_ID = os.environ.get('ADMIN_ID', '')
WEB_APP_URL = 'https://bekbolat00.github.io/sun-app/'

# Отключаем потоки, чтобы Vercel не убивал процесс раньше времени
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"--- НОВЫЙ ЮЗЕР: {message.from_user.first_name} (ID: {message.from_user.id}) ---")
    
    # 1. Отправляем Сане
    try:
        username = message.from_user.username
        username_str = f"@{username}" if username else "скрыт"
        admin_text = f"🚨 *Новый запуск бота!*\n\nИмя: {message.from_user.first_name}\nНик: {username_str}\nID: `{message.from_user.id}`"
        bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode='Markdown')
        print("УСПЕХ: Уведомление админу отправлено")
    except Exception as e:
        print(f"ОШИБКА АДМИНУ: {e}")
        
    # 2. Отправляем Юзеру
    try:
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("⚡️ Открыть SUN App", web_app=telebot.types.WebAppInfo(url=WEB_APP_URL))
        markup.add(btn)
        bot.send_message(message.chat.id, "Добро пожаловать в SUN! Твоя база знаний готова к работе 👇", reply_markup=markup)
        print("УСПЕХ: Сообщение юзеру отправлено")
    except Exception as e:
        print(f"ОШИБКА ЮЗЕРУ: {e}")

# Универсальный роутер для Телеграма (POST) и для Браузера (GET)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(">>> Получен POST вебхук от Telegram")
        try:
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return 'OK', 200
        except Exception as e:
            print(f"ОШИБКА ВЕБХУКА: {e}")
            return 'Error', 500
    else:
        # Это сработает, если ты просто откроешь ссылку Vercel в браузере
        return '<h1>Бот SUN успешно работает на Vercel! 🚀</h1>', 200
