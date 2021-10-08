import telebot
import local_configs as config
from search import *
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum

from telegram_bot_pagination import InlineKeyboardPaginator

bot = telebot.TeleBot(config.telegram_token)
module_to_find = ""


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Herzlich Willkommen! Hier können Sie alle Module finden, die auf Moses zur Verfügung stehen, und die wichtigste Info über sie. Auch Sie können Bewertung für jedes Modul anschauen und selbst ein Feedback lassen, wenn Sie was zu sagen haben. Viel Spaß!")


@bot.message_handler(func=lambda m: True, content_types=["text"])
def show_modules(message, page=1):
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
            paginator.add_after(InlineKeyboardButton(f'{modules[i][2]}', callback_data=i))

        bot.send_message(message.chat.id, "*Ergebnisse:*", parse_mode='Markdown',
                         reply_markup=paginator.markup)
    except IndexError:
        bot.send_message(message.chat.id, "Keine Module gefunden :(")


def generate_paginator(page_count, page=1):
    paginator = InlineKeyboardPaginator(
            page_count=page_count,
            current_page=page,
            data_pattern='page#{page}'
        )
    return paginator.markup


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
    modules = find_modules(module_to_find)
    module = modules[int(call.data)]
    nummer = module[0].split(" / ")[0]
    version = module[0].split(" / ")[1]
    link = f"https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/beschreibung/anzeigen.html?nummer={nummer}&version={version}&sprache=1"
    info = find_specific_module(link)
    bot.send_message(call.message.chat.id,
                     f"*Titel des Moduls:* {info['titel']} \n"
                     f"*Leistungspunkte:* {info['lp']} \n"
                     f"*Modul/Version:* {info['modul/version']} \n"
                     f"*Verantwortliche Person:* {info['verantwortliche']} \n"
                     f"*E-Mail-Adresse:* {info['email']} \n"
                     f"*Lernergebnisse:* {info['lernergebnisse']} \n \n"
                     f"*Lehrinhalte:* {info['lehrinhalte']}",
                     parse_mode="Markdown")
    print(info)

bot.polling()