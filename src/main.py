import telebot
import local_configs as config
from search import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(config.telegram_token)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 6
    markup.add(InlineKeyboardButton("1", callback_data="1"),
               InlineKeyboardButton("2", callback_data="2"),
               InlineKeyboardButton("3", callback_data="3"),
               InlineKeyboardButton("4", callback_data="4"),
               InlineKeyboardButton("5", callback_data="5"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "Modul ausgewählt")


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Herzlich Willkommen! Hier können Sie alle Module finden, die auf Moses zur Verfügung stehen, und die wichtigste Info über sie. Auch Sie können Bewertung für jedes Modul anschauen und selbst ein Feedback lassen, wenn Sie was zu sagen haben. Viel Spaß!")


@bot.message_handler(func=lambda m: True, content_types=["text"])
def show_modules(message):
    try:
        modules = find_modules(message.text)
        text = ""
        for i in range(len(modules)):
            text += "*" + str(i + 1) + ".* " + modules[i] + "\n"
        bot.send_message(message.chat.id, "Ergebnisse: \n" + text, parse_mode='Markdown', reply_markup=gen_markup())
    except IndexError:
        bot.send_message(message.chat.id, "Keine Module gefunden :(")

bot.polling()