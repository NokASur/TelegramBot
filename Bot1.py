import os
import telebot
import random
from telebot import types

TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    sticker = open('img/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    chat1 = types.KeyboardButton("Как дела?")
    chat2 = types.KeyboardButton("Какие новости?")
    markup.add(chat1, chat2)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n"
                                      "Я - <b>{1.first_name}</b>".format(message.from_user, bot.get_me()),
                     parse_mode="html", reply_markup=['text'])


@bot.message_handler(content_types=['text'])
def bla(message):
    if message.chat.type == "private":
        if message.text == "Как дела?":
            bot.send_message(message.chat.id, "Отлично,{0.first_name}, как сам?")
        else:
            bot.send_message(message.chat.id, "Иди лучше решай серии, а не вбрасывай сюда всякую фигню,{0.first_name}")


bot.polling(none_stop=True)
