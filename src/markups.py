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
    markup.add(InlineKeyboardButton("Das Modul bewerten", callback_data="bewerten"))
    return markup


def report_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Report", callback_data="report"))
    return markup



# def approval_markup():
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 2
#     markup.add(InlineKeyboardButton("Approve", callback_data="approve"))
#     markup.add(InlineKeyboardButton("Deny", callback_data="deny"))
#     return markup
