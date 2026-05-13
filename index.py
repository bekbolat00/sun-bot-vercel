import os
import json
import urllib.request
from flask import Flask, request

# Достаем ключи из Vercel
TOKEN = os.environ.get('BOT_TOKEN', '').strip()
ADMIN_ID = os.environ.get('ADMIN_ID', '').strip()
WEB_APP_URL = 'https://bekbolat00.github.io/sun-app/'

app = Flask(__name__)

# Прямая функция-пушка для отправки в обход библиотек
def send_telegram_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
        
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        # Сервер Vercel будет ждать, пока Телеграм не примет сообщение
        urllib.request.urlopen(req, timeout=5)
        print(f"Успешно отправлено в чат {chat_id}")
    except Exception as e:
        print(f"Ошибка API Телеграма: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            data = request.json
            if data and "message" in data and "text" in data["message"]:
                text = data["message"]["text"]
                chat_id = data["message"]["chat"]["id"]
                
                if text == "/start":
                    user_id = data["message"]["from"].get("id", "")
                    first_name = data["message"]["from"].get("first_name", "Ученик")
                    username = data["message"]["from"].get("username", "")
                    username_str = f"@{username}" if username else "скрыт"
                    
                    # 1. Отправляем Сане
                    admin_text = f"🚨 *Новый запуск бота!*\n\nИмя: {first_name}\nНик: {username_str}\nID для таблицы: `{user_id}`\n\n_(Нажми на цифры ID, чтобы скопировать)_"
                    send_telegram_message(ADMIN_ID, admin_text)
                    
                    # 2. Отправляем Пользователю
                    markup = {
                        "inline_keyboard": [[
                            {"text": "⚡️ Открыть SUN App", "web_app": {"url": WEB_APP_URL}}
                        ]]
                    }
                    user_text = "Добро пожаловать в SUN! Твоя база знаний готова к работе 👇"
                    send_telegram_message(chat_id, user_text, reply_markup=markup)
                    
        except Exception as e:
            print(f"Ошибка кода: {e}")
            
        return 'OK', 200
    else:
        return '<h1>SUN Serverless Bot работает! 🚀</h1>', 200
