import db
import telebot
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    but_read = telebot.types.KeyboardButton(text='/read')
    markup.add(but_add, but_read)
    db.DbQuery().add_user(message.from_user.id)
    bot.send_message(message.chat.id, 'Привет, я чат-бот для самых смешных анекдотов. Нажми на кнопку /read, чтобы читать смешные анекдоты', reply_markup=markup)



@bot.message_handler(commands=['read'])
def read(message):
    joke = db.DbQuery().get_random_joke(message.chat.id)
    bot.send_message(message.chat.id, joke[1])


@bot.message_handler(commands=['reset'])
def reset(message):
    db.DbQuery().reset(message.chat.id)
    bot.send_message(message.chat.id, 'База данных просмотренных анекдотов была удалена')


bot.infinity_polling()