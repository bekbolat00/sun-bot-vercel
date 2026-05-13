import os
import json
import urllib.request
from flask import Flask, request, jsonify

TOKEN = os.environ.get('BOT_TOKEN', '').strip()
ADMIN_ID = os.environ.get('ADMIN_ID', '').strip()
WEB_APP_URL = 'https://bekbolat00.github.io/sun-app/'

app = Flask(__name__)

# Функция с "прослушкой" от твоего друга
def notify_admin(first_name, username_str, user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    text = f"🚨 *Новый запуск бота!*\n\nИмя: {first_name}\nНик: {username_str}\nID для таблицы: `{user_id}`\n\n_(Нажми на цифры ID, чтобы скопировать)_"
    payload = {"chat_id": ADMIN_ID, "text": text, "parse_mode": "Markdown"}
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            # Если всё прошло успешно, увидим статус 200
            print(f"ОТВЕТ ТЕЛЕГРАМА (Сана): {response.status} {response.read().decode()}")
    except Exception as e:
        # Если Телеграм или Vercel ругнулись, увидим точную причину
        print(f"ОШИБКА ОТПРАВКИ (Сана): {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            data = request.json
            if data and "message" in data:
                msg = data["message"]
                if "text" in msg and msg["text"] == "/start":
                    chat_id = msg["chat"]["id"]
                    user_id = msg["from"].get("id", "")
                    first_name = msg["from"].get("first_name", "Ученик")
                    username = msg["from"].get("username", "")
                    username_str = f"@{username}" if username else "скрыт"
                    
                    # 1. Отправляем Сане (через функцию с логами)
                    notify_admin(first_name, username_str, user_id)
                    
                    # 2. Отвечаем тебе прямо в теле вебхука (безотказный метод)
                    return jsonify({
                        "method": "sendMessage",
                        "chat_id": chat_id,
                        "text": "Добро пожаловать в SUN! Твоя база знаний готова к работе 👇",
                        "reply_markup": {
                            "inline_keyboard": [[
                                {"text": "⚡️ Открыть SUN App", "web_app": {"url": WEB_APP_URL}}
                            ]]
                        }
                    })
        except Exception as e:
            print(f"ОШИБКА КОДА: {e}")
            
        return 'OK', 200
    else:
        return '<h1>SUN Bot is alive! 🚀</h1>', 200
