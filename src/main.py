import telebot
import local_configs as config
#import env_configs as config
from search import *
# from telebot import types
import os
import logging
from flask import Flask, request
from telebot import custom_filters
from telegram_bot_pagination import InlineKeyboardPaginator

from reviews import save_review_database, get_all_reviews
from markups import generate_paginator, gen_review_markup

bot = telebot.TeleBot(config.telegram_token)
module_to_find = ""
module_id = 0


class States:
    reading = 1
    writing = 2


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Herzlich Willkommen! Hier können Sie alle Module finden, die auf Moses zur Verfügung stehen, und die wichtigste Info über sie. Auch Sie können Bewertung für jedes Modul anschauen und selbst ein Feedback lassen, wenn Sie was zu sagen haben. Viel Spaß!")
    bot.set_state(message.chat.id, States.reading)


@bot.message_handler(state=States.writing)
def save_review(message):
    global module_id
    #bot.send_message(message.chat.id, message.text) #return a message itself for test purposes
    save_review_database(module_id, message.text)
    bot.set_state(message.chat.id, States.reading)
    bot.send_message(message.chat.id, "Vielen Dank für deine Rückmeldung. Sie wird demnächst veröffentlicht!")
    module_id = 0


@bot.message_handler(func=lambda m: True, content_types=["text"])
def show_modules(message, page=1):
    bot.set_state(message.chat.id, States.reading)
    try:
        global module_to_find
        module_to_find = message
        modules = find_modules(message)
        total_pages = int(len(modules) / 10 + (len(modules) % 10 > 0))
        paginator = InlineKeyboardPaginator(
            page_count=total_pages,
            current_page=page,
            data_pattern="page#{page}"
        )

        for i in range((page-1) * 10, (page-1) * 10 + (len(modules) % 10)*(page == total_pages) + 10*(page != total_pages)):
            paginator.add_after(telebot.types.InlineKeyboardButton(f'{modules[i][2]}', callback_data=i))

        bot.send_message(message.chat.id, "*Ergebnisse:*", parse_mode='Markdown',
                         reply_markup=paginator.markup)
    except IndexError:
        bot.send_message(message.chat.id, "Keine Module gefunden :(")


@bot.callback_query_handler(func=lambda call: call.data =='bewertungen')
def show_reviews(call):
    reviews = get_all_reviews(module_id)
    bot.send_message(call.message.chat.id, reviews, parse_mode="HTML")


# @bot.callback_query_handler(func=lambda call: call.data =='approve')
# def approve_review(call):
#     reviews = get_all_reviews(module_id)
#     bot.send_message(call.message.chat.id, reviews)


@bot.callback_query_handler(func=lambda call: call.data =='bewerten')
def get_review(call):
    bot.send_message(call.message.chat.id, "Schreiben Sie Ihre Rezension!")
    bot.set_state(call.message.chat.id, States.writing)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='page')
def characters_page_callback(call):
    global module_to_find
    page = int(call.data.split('#')[1])
    print(page)
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    show_modules(module_to_find, page)


@bot.callback_query_handler(func=lambda call: True)
def show_specific_module(call):
    global module_id
    modules = find_modules(module_to_find)
    module = modules[int(call.data)]
    nummer = module[0].split(" / ")[0]
    version = module[0].split(" / ")[1]
    link = f"https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/beschreibung/anzeigen.html?nummer={nummer}&version={version}&sprache=1"
    info = find_specific_module(link)
    module_id = nummer
    bot.send_message(call.message.chat.id,
                     f"<b>Titel des Moduls:</b> {info['titel']} \n"
                     f"<b>Leistungspunkte:</b> {info['lp']} \n"
                     f"<b>Modul/Version:</b> {info['modul/version']} \n"
                     f"<b>Verantwortliche Person:</b> {info['verantwortliche']} \n"
                     f"<b>E-Mail-Adresse:</b> {info['email']} \n"
                     f"<b>Lernergebnisse:</b> {info['lernergebnisse']} \n \n"
                     f"<b>Lehrinhalte:</b> {info['lehrinhalte']}",
                     parse_mode="HTML", reply_markup=gen_review_markup())
    print(info)


# def approve_message(review):
#     bot.send_message(206662948, review, reply_markup=approval_markup())


bot.add_custom_filter(custom_filters.StateFilter(bot))

    
# check if heroku variable is in the environment
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)

    @server.route("/", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=config.app_url)
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # without heroku variable local use
    # delete webhook and use long polling
    bot.remove_webhook()
    bot.polling(none_stop=True)