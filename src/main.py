import telebot
#import local_configs as config
import env_configs as config
from search import *
import os
import logging
from flask import Flask, request
from telebot import custom_filters
from telegram_bot_pagination import InlineKeyboardPaginator

from reviews import save_review_database, reviews_in_total, modules_in_total, reviewed_modules, save_star_database, calculate_average_star, get_all_reviews_list, get_all_semester_for_module
from markups import gen_review_markup, stars_markup, grade_markup

bot = telebot.TeleBot(config.telegram_token)
module_to_find = ""
module_id = 0
module_name = ""
semester = ""


class States:
    reading = 1
    writing = 2
    getting_semester = 3


# BASIC SECTION #
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Um ein nötiges Modul zu finden, schreib einfach den offiziellen Namen, ein Teil reicht auch. \n\n"
                                      "Wenn du aber Modul bewerten willst, könnte das hilfreich sein:\n" 
                                      "- Schreib etwas, was du selbst gewusst hättest, bevor das Modul auszuwählen\n"
                                      "- Welche Tutoren nach deiner Meinung gut waren, welche nicht\n"
                                      "- Was prüfungsrelevant ist, welche Feinheiten es gibt\n"
                                      "- Inwiefern das Modul wirklich aufwendig ist\n"
                                      "- Ob es überhaupt Spaß gemacht hat oder es eher um Bestehen und Vergessen ging\n"
                                      "- Vermeide jegliche Art von Beleidigungen")
    bot.set_state(message.chat.id, States.reading)


@bot.message_handler(commands=['stats'])
def show_stats(message):
    bot.send_message(message.chat.id,
                     f"Es wurden schon *{reviews_in_total()}* Rezensionen geschrieben"
                    f" und *{modules_in_total()}* Module insgesamt bewertet!",
                    parse_mode="Markdown")


@bot.message_handler(commands=['modules'])
def show_reviewed_modules(message):
    modules = reviewed_modules()
    bot.send_message(message.chat.id,
                     modules,
                     parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data =='report')
def send_report(call):
    bot.send_message(call.message.chat.id, "Danke, Report wurde gesendet!")
    bot.send_message(206662948, f"*Report ist eingegangen.* \n"
                                f"Schau mal in die Bewertungen von *{module_name}* an.",
                     parse_mode="Markdown")


# WRITE REVIEW SECTION #
@bot.callback_query_handler(func=lambda call: call.data =='bewerten')
def get_semester(call):
    bot.send_message(call.message.chat.id, "In welchem Semester wurde das Modul abgelegt? Schicken Sie einzelne Nachricht im folgenden Format 'WiSe20/21'.")
    bot.set_state(call.message.chat.id, States.getting_semester)


@bot.message_handler(state=States.getting_semester)
def get_review(message):
    bot.set_state(message.chat.id, States.writing)
    global semester
    semester = message.text
    bot.send_message(message.chat.id, "Schreiben Sie Ihre Rezension!")


@bot.message_handler(state=States.writing)
def save_review(message):
    if save_review_database(module_id, message.text, module_name, semester, message.chat.id):
        bot.set_state(message.chat.id, States.reading)
        bot.send_message(message.chat.id, "Vielen Dank für deine Rückmeldung. Sie wird demnächst veröffentlicht!")
    else:
        bot.set_state(message.chat.id, States.reading)
        bot.send_message(message.chat.id, "Man darf mehr als eine Rezension für das Modul nicht schreiben.")


# SHOW REVIEWS SECTION #
@bot.callback_query_handler(func=lambda call: call.data =='bewertungen')
def show_reviews_list(call, page=1):
    average_star = calculate_average_star(module_id)
    print(module_id, average_star)
    if average_star is None:
        reviews = f"Leider gibt es noch keine Bewertungen."
        bot.send_message(call.message.chat.id, reviews, parse_mode="HTML", reply_markup=grade_markup())
    else:
        to_print = f"Durchschnittsnote ist {round(average_star, 1)} ⭐ / 5 ⭐ \n\n"
        semesters = get_all_semester_for_module(module_id, module_name)
        to_print += semesters[page-1]
        to_print += "\n\n"
        reviews = get_all_reviews_list(module_id, module_name)
        paginator = InlineKeyboardPaginator(
            page_count=len(reviews),
            current_page=page,
            data_pattern="review#{page}"
        )
        paginator.add_after(telebot.types.InlineKeyboardButton('Report', callback_data="report"))
        bot.send_message(call.message.chat.id, to_print + reviews[page-1], parse_mode="HTML", reply_markup=paginator.markup)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='review')
def reviews_page_callback(call):
    global module_to_find
    page = int(call.data.split('#')[1])
    print(page)
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    show_reviews_list(call, page)


# STAR SECTION #
@bot.callback_query_handler(func=lambda call: call.data =='stars')
def give_star(call):
    print(call)
    bot.send_message(call.message.chat.id,
                     "Geben Sie die Anzahl von Sternen für dieses Modul!\n\n"
                     "5 - Gut gemacht. Würde sogar aus Spaß wiederholen\n"
                     "4 - Ziemlich nice, aber leider nicht ideal\n"
                     "3 - Passt. Gibt bessere, aber auch schlechtere\n"
                     "2 - Naja, hätte nicht abgelegt\n"
                     "1 - Albtraum. Nie wieder.",
                     reply_markup=stars_markup())


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='star')
def save_star(call):
    star = int(call.data.split('#')[1])
    if (save_star_database(module_id, module_name, star, call.message.chat.id) == "success"):
        bot.send_message(call.message.chat.id,
                            "Danke, deine Bewertung wurde gespeichert.")
    else:
        bot.send_message(call.message.chat.id,
                         "Das Modul wurde schon bewertet.")


# MODULES SECTION #
@bot.message_handler(func=lambda m: True, content_types=["text"])
def show_modules(message, page=1):
    bot.set_state(message.chat.id, States.reading)
    global module_id, module_name
    module_id = 0
    module_name = ""
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
    global module_id, module_name
    modules = find_modules(module_to_find)
    module = modules[int(call.data)]
    nummer = module[0].split("\n")[0]
    version = module[0].split("\n")[1].replace("(", "").replace(")", "")
    link = f"https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/beschreibung/anzeigen.html?nummer={nummer}&version={version}&sprache=1"
    info = find_specific_module(link)
    module_id = nummer
    module_name = info['titel']
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