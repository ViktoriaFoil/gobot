import os
import time
import datetime
import logging
from threading import Thread

import telebot

from config.mysql import close_connect_db
from logs.log import log
from main import Parsing
from objects.userbot import User
from queries_to_tables.tournament_go import Tournament_go
from queries_to_tables.user_botgo import User_botgo
from queries_to_tables.usercity import User_City
from stages.age_category import Age_category
from stages.city_selection_chenge import City_selection_chenge
from stages.massage_to_developer import Message_to_developer
from stages.state_main import State_main

token = os.getenv("BOT")
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def message(message):
    state = "city_selection"
    users = User(chat_id=message.chat.id,
                 first_name=message.chat.first_name,
                 last_name=message.chat.last_name,
                 username=message.chat.username,
                 state=state)

    User_botgo.query_users(users)

    SelectState = User_botgo(message.chat.id).selectState()

    if SelectState == "city_selection":
        City_selection_chenge().message_state_city_selection(message)
        return

    if SelectState == "change_city":
        City_selection_chenge().message_state_city_change(message)
        return

    if SelectState == "age_category":
        Age_category().message_state_age_category(message)
        return

    if SelectState == "main":
        State_main.message_state_main(message)
        return

    if SelectState == "message_to_developer" and \
            message.text.lower() != "/message_to_developer" and \
            message.text.lower() != "сообщение автору":
        Message_to_developer().mess_to_dev(message)
        return


# =======================================================================================================
# =======================================================================================================


def push_message():
    try:
        all_users = User_botgo.all_users()
        for chatID in all_users:
            if User_botgo(chatID).is_user_child():
                for tournament in Tournament_go(chatID).tournaments_for_user():
                    bot.send_message(chatID, "В твоем городе появился турнир \n\n" + tournament)
                    log(chatID, "a new children's tournament has been sent", logging.INFO)
            else:
                for tournament in Tournament_go(chatID).tournaments_for_user_adult():
                    bot.send_message(chatID, "В твоем городе появился турнир \n\n" + tournament)
                    log(chatID, "new tournament sent", logging.INFO)

    except AssertionError():
        print("!!!!!!! user has been blocked !!!!!!!")
    except BaseException as e:
        log(0, f"error {e}", logging.ERROR)


def notification_of_details():
    try:
        all_users = User_botgo.all_users()
        for chatID in all_users:
            if User_botgo(chatID).is_user_child():
                for tournament in Tournament_go(chatID).details_of_tournament_exist_for_user():
                    bot.send_message(chatID, "У этого турнира появились подробности \n\n" + tournament)
                    Tournament_go.update_tournament_details()
                    log(chatID, "details children's tournament has been sent", logging.INFO)
            else:
                for tournament in Tournament_go(chatID).details_of_tournament_exist_for_user_adult():
                    bot.send_message(chatID, "У этого турнира появились подробности \n\n" + tournament)
                    Tournament_go.update_tournament_details()
                    log(chatID, "details tournament sent", logging.INFO)

    except AssertionError():
        print("!!!!!!! user has been blocked !!!!!!!")
    except BaseException as e:
        log(0, f"error {e}", logging.ERROR)


def background():
    while True:
        Parsing.download_page("https://gofederation.ru/tournaments/", "APP/html/current.html"),
        Parsing.compare("APP/html/current.html", "APP/html/old.html"),
        Parsing.copy_current_to_old("APP/html/old.html", "APP/html/current.html"),

        if Tournament_go.number_of_entries():
            Parsing.main(True)
        else:
            Parsing.main(False)

        # рассылка новых турниров
        push_message(),
        # поменять статус новых турниров на обычный
        Tournament_go.change_new_to_notified(),
        # удалить старые турниры
        Tournament_go.delete_old_tournaments(),
        # проверка, появились ли подробности турниров
        Tournament_go.check_details(),
        # если есть детали, то отправить
        notification_of_details(),
        now = datetime.datetime.now()

        if now.month == 12:
            nextyear = now.year + 1
            Parsing.download_page(f"https://gofederation.ru/tournaments?year={nextyear}", "APP/html/current.html"),
            Parsing.compare("APP/html/current.html", "APP/html/old.html"),
            Parsing.copy_current_to_old("APP/html/old.html", "APP/html/current.html"),
            Parsing.main(False),
            push_message(),
            Tournament_go.change_new_to_notified()

        log(0, "stop cycle for 60 seconds", logging.INFO)
        time.sleep(60)


if __name__ == '__main__':
    t1 = Thread(target=background, args=())
    t1.start()
    bot.polling(none_stop=True)
    close_connect_db()
