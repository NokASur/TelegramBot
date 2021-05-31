import os
import telebot


TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n"
                     "Я - <b>{1.first_name}</b>".format(message.from_user, bot.get_me()),
                     parse_mode="html")
    sticker = open('img/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)


@bot.message_handler(content_types=['text'])
def bla(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
