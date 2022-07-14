import db
import telebot
from telebot import types
bot = telebot.TeleBot('5343235488:AAEmX__rzBe8r1nFM1GRQtzKLY3cqT0Zywc')

id = None
id_prev = None
param_like = 1
param_dislike = 1

@bot.message_handler(content_types=['text'], commands=['start'])
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    but_read = types.KeyboardButton('/read')
    but_add = types.KeyboardButton('/add')
    markup.add(but_add, but_read)
    db.DbQuery().add_user(message.from_user.id)
    bot.send_message(message.chat.id, 'Привет, я чат-бот для самых смешных анекдотов. Нажми на кнопку /read, чтобы читать смешные анекдоты', reply_markup=markup)



@bot.message_handler(content_types=['text'], commands=['read'])
def read(message):
    joke = db.DbQuery().get_random_joke(message.chat.id)
    global id, id_prev
    id_prev = id
    id = joke[0]
    markup=types.InlineKeyboardMarkup(row_width=2)
    like, dislike = db.DbQuery().get_likes_and_dislikes(id)
    but_like=types.InlineKeyboardButton('👍 (' +str(like) + ')' , callback_data='+1')
    but_dislike=types.InlineKeyboardButton('👎 ('+str(dislike) + ')', callback_data='-1')
    markup.add(but_like, but_dislike)
    bot.send_message(message.chat.id, joke[1], reply_markup=markup)


def par(n):
    if n == -1:
        return 1
    elif n == 1:
        return -1

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    global id, id_prev, param_dislike, param_like
    if id == id_prev:
        param_like = par(param_like)
        param_dislike = par(param_dislike)
    else:
        param_like = 1
        param_dislike = 1
    if call.data == '+1':
        if param_like == 1:
            bot.send_message(call.from_user.id, "Вы поставили лайк")
        elif param_like == -1:
            bot.send_message(call.from_user.id, "Вы убрали лайк")
        bot.answer_callback_query(call.id)
        db.DbQuery().change_likes(id, bool=param_like)
    elif call.data == '-1':
        if param_dislike == 1:
            bot.send_message(call.from_user.id, "Вы поставили дизлайк")
        elif param_dislike == -1:
            bot.send_message(call.from_user.id, "Вы убрали дизлайк")
        bot.answer_callback_query(call.id)
        db.DbQuery().change_dislikes(id, bool=param_dislike)
    id_prev = id


@bot.message_handler(content_types=['text'], commands=['add'])
def add(message):
    bot.send_message(message.chat.id, 'Напишите свой анекдот, и он попадёт в мою базу данных')
    @bot.message_handler(content_types=['text'])
    def write_joke(msg):
        db.DbQuery().insert_joke(joke_text=msg.text)
        bot.send_message(msg.chat.id, 'Отлично, ваш анекдот в общей базе данных')


@bot.message_handler(content_types=['text'], commands=['reset'])
def reset(message):
    db.DbQuery().reset(message.chat.id)
    bot.send_message(message.chat.id, 'База данных просмотренных анекдотов была удалена')


bot.polling(none_stop=True)