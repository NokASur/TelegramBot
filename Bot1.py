import os
import telebot
from telebot import types
import feedparser


def feed_parser():
    newsfeed = {'РосРеестр': 'https://rosreestr.ru/site/rss/',
                'Федеральная Налоговая Служба': 'https://www.nalog.ru/rn62/rss/'}
    message = dict()
    for key in newsfeed.keys():
        current_news = feedparser.parse(newsfeed[key]).entries[0]
        message[key] = current_news.title + '\n' + current_news.link
    return message


TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    sticker = open('img/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    chat1 = types.KeyboardButton("Как дела?")
    chat2 = types.KeyboardButton("Какие новости?")
    chat3 = types.KeyboardButton("♂Кто писал бо(y)ту♂")
    keyb.add(chat1, chat2, chat3)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n"
                                      "Я - <b>{1.first_name}</b>".format(message.from_user, bot.get_me()),
                     parse_mode="html", reply_markup=keyb)


@bot.message_handler(content_types=['text'])
def bla(message):
    if message.chat.type == "private":
        if message.text == "Как дела?":
            ans = types.InlineKeyboardMarkup(row_width=2)
            ans1 = types.InlineKeyboardButton("Хорошо", callback_data="good")
            ans2 = types.InlineKeyboardButton("Плохо", callback_data="bad")
            ans.add(ans1, ans2)
            bot.send_message(message.chat.id,
                             "Отлично, {0.first_name}, как сам?".format(message.from_user, bot.get_me()),
                             reply_markup=ans)

        elif message.text == "♂Кто писал бо(y)ту♂":
            bot.send_message(message.chat.id, "Нельзя просто так взять и реализовать базу данных")

        elif message.text == "Какие новости?":
            post = feed_parser()
            bot.send_message(message.chat.id, 'Новая информация на выбранных площадках:')
            for key in post.keys():
                bot.send_message(message.chat.id, key + '\n' + post[key])

        else:
            bot.send_message(message.chat.id,
                             "Иди лучше решай серии, а не вбрасывай сюда всякую фигню, {0.first_name}".format(
                                 message.from_user, bot.get_me()))


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        if call.message:
            if call.data == "good":
                bot.send_message(call.message.chat.id, 'Я очень этому рад')
            elif call.data == "bad":
                bot.send_message(call.message.chat.id, 'Очень жаль')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Как дела?",
                                  reply_markup=None)
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)

