from telegram_bot_pagination import InlineKeyboardPaginator
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_paginator(page_count, page=1):
    paginator = InlineKeyboardPaginator(
            page_count=page_count,
            current_page=page,
            data_pattern='page#{page}'
        )
    return paginator.markup


def gen_review_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Bewertungen", callback_data="bewertungen"))
    markup.add(InlineKeyboardButton("Rezension schreiben", callback_data="bewerten"))
    markup.add(InlineKeyboardButton("Das Modul bewerten", callback_data="stars"))
    return markup


def report_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Report", callback_data="report"))
    return markup


def stars_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 5
    markup.add(InlineKeyboardButton("1 ⭐", callback_data="star#1"),
               InlineKeyboardButton("2 ⭐", callback_data="star#2"),
               InlineKeyboardButton("3 ⭐", callback_data="star#3"),
               InlineKeyboardButton("4 ⭐", callback_data="star#4"),
               InlineKeyboardButton("5 ⭐", callback_data="star#5"))
    return markup
