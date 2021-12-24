from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_review_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Bewertungen und Rezensionen", callback_data="bewertungen"))
    markup.add(InlineKeyboardButton("Rezension schreiben", callback_data="bewerten"))
    markup.add(InlineKeyboardButton("Das Modul bewerten", callback_data="stars"))
    markup.add(InlineKeyboardButton("Notenschlüssel", callback_data="gradekey"))
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


def grade_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 5
    markup.add(InlineKeyboardButton("Das Modul bewerten", callback_data="stars"))
    return markup