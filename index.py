import os
import telebot
from flask import Flask, request

# Достаем ключи
TOKEN = os.environ.get('BOT_TOKEN', '')
ADMIN_ID = os.environ.get('ADMIN_ID', '')
WEB_APP_URL = 'https://bekbolat00.github.io/sun-app/'

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Читаем данные напрямую от Телеграма в обход очередей
            data = request.json
            
            # Проверяем, что нам прислали текст
            if data and "message" in data and "text" in data["message"]:
                text = data["message"]["text"]
                chat_id = data["message"]["chat"]["id"]
                
                # Если нажали /start
                if text == "/start":
                    user_id = data["message"]["from"].get("id", "")
                    first_name = data["message"]["from"].get("first_name", "Ученик")
                    username = data["message"]["from"].get("username", "")
                    username_str = f"@{username}" if username else "скрыт"
                    
                    # 1. ПРЯМАЯ ОТПРАВКА САНЕ (Без очередей)
                    try:
                        admin_text = f"🚨 *Новый запуск бота!*\n\nИмя: {first_name}\nНик: {username_str}\nID для таблицы: `{user_id}`\n\n_(Нажми на цифры ID, чтобы скопировать)_"
                        bot.send_message(ADMIN_ID, admin_text, parse_mode='Markdown')
                    except Exception as e:
                        print(f"Ошибка отправки Сане: {e}")
                        
                    # 2. ПРЯМАЯ ОТПРАВКА ТЕБЕ (Юзеру)
                    try:
                        markup = telebot.types.InlineKeyboardMarkup()
                        btn = telebot.types.InlineKeyboardButton("⚡️ Открыть SUN App", web_app=telebot.types.WebAppInfo(url=WEB_APP_URL))
                        markup.add(btn)
                        bot.send_message(chat_id, "Добро пожаловать в SUN! Твоя база знаний готова к работе 👇", reply_markup=markup)
                    except Exception as e:
                        print(f"Ошибка отправки Юзеру: {e}")
                        
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            
        # Только после отправки сообщений разрешаем Vercel уснуть
        return 'OK', 200
    else:
        return '<h1>Сервер SUN работает! 🚀</h1>', 200
