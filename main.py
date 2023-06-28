import db
import telebot
from telebot import types
bot = telebot.TeleBot('5343235488:AAEmX__rzBe8r1nFM1GRQtzKLY3cqT0Zywc')


@bot.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    but_read = types.KeyboardButton(text='/read')
    but_add = types.KeyboardButton(text='/add')
    markup.add(but_add, but_read)
    db.DbQuery().add_user(message.from_user.id)
    bot.send_message(message.chat.id, 'Привет, я чат-бот для самых смешных анекдотов. Нажми на кнопку /read, чтобы читать смешные анекдоты', reply_markup=markup)



@bot.message_handler(commands=['read'])
def read(message):
    joke = db.DbQuery().get_random_joke(message.chat.id)
    bot.send_message(message.chat.id, joke[1])



@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, 'Напишите свой анекдот, и он попадёт в мою базу данных')
    @bot.message_handler(content_types=['text'])
    def write_joke(msg):
        db.DbQuery().insert_joke(joke_text=msg.text)
        bot.send_message(msg.chat.id, 'Отлично, ваш анекдот в общей базе данных')


@bot.message_handler(commands=['reset'])
def reset(message):
    db.DbQuery().reset(message.chat.id)
    bot.send_message(message.chat.id, 'База данных просмотренных анекдотов была удалена')


bot.infinity_polling()