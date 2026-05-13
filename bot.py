import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# ВАЖНО: Вставь сюда свой токен от BotFather (внутри кавычек)
TOKEN = '7773036562:AAG37ouLY3a-Bw-we8ZE7I6Bz_SZZvLlit8'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    # Создаем клавиатуру с кнопкой
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Ссылка на твой сайт на GitHub (с хвостиком ?v=4 для сброса кэша)
    web_app = WebAppInfo(url="https://bekbolat00.github.io/sun-mini-app/?v=5") 
    
    # Сама кнопка
    button = KeyboardButton(text="Открыть SUN App ☀️", web_app=web_app)
    markup.add(button)
    
    # Сообщение от бота
    bot.send_message(
        message.chat.id, 
        "Добро пожаловать в SUN! Нажми кнопку ниже, чтобы открыть приложение 👇", 
        reply_markup=markup
    )

if __name__ == '__main__':
    print("Бот успешно запущен! Открой Telegram и напиши ему /start")
    bot.infinity_polling()