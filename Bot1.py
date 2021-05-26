import os
import telebot


TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def bla(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
