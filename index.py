import os
import json
import urllib.request
from flask import Flask, request, jsonify

TOKEN = os.environ.get('BOT_TOKEN', '').strip()
ADMIN_ID = os.environ.get('ADMIN_ID', '').strip()
WEB_APP_URL = 'https://bekbolat00.github.io/sun-bot-vercel'

app = Flask(__name__)

def notify_admin(first_name, username_str, user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    text = f"🚨 *Новый запуск бота!*\n\nИмя: {first_name}\nНик: {username_str}\nID для таблицы: `{user_id}`\n\n_(Нажми на цифры ID, чтобы скопировать)_"
    payload = {"chat_id": ADMIN_ID, "text": text, "parse_mode": "Markdown"}
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"Ошибка админу: {e}")

# МАГИЯ: Ловим ВООБЩЕ ВСЕ пути (и /, и /api, и любые другие)
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
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
                    
                    # 1. Пишем Сане
                    notify_admin(first_name, username_str, user_id)
                    
                    # 2. Моментально отвечаем юзеру
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
            print(f"Ошибка: {e}")
            
        return 'OK', 200
    else:
        return '<h1>SUN Bot API работает на 100%! 🚀</h1>', 200
