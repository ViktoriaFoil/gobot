import os
import time
import datetime
import logging
from threading import Thread

import telebot as telebot

from APP.config.mysql import Mysql
from APP.logs.log import log
from APP.main import Parsing
from APP.objects.userbot import User
from APP.queries_to_tables.tournament_go import Tournament_go
from APP.queries_to_tables.user_botgo import User_botgo
from APP.queries_to_tables.usercity import User_City
from APP.stages.age_category import Age_category
from APP.stages.city_selection_chenge import City_selection_chenge
from APP.stages.massage_to_developer import Message_to_developer
from APP.stages.state_main import State_main

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

    user_botgo = User_botgo(message.chat.id)
    SelectState = user_botgo.selectState()

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
        for new_tournaments in Tournament_go.get_new_tournaments():
            for UserCity in User_City(message.chat.id).get_user_subscription_city():
                if new_tournaments[3] == UserCity[1]:
                    if User_botgo(message.chat.id).is_user_child():
                        for tournament in Tournament_go(message.chat.id).tournaments_for_user():
                            chatID = User_botgo(message.chat.id).get_ChatId_By_UserId()
                            bot.send_message(chatID, "В твоем городе появился турнир \n\n" + tournament)
                            log(message.chat.id, "a new children's tournament has been sent", logging.INFO)

                    else:  # иначе пользователь взрослый
                        for tournament in Tournament_go(message.chat.id).tournaments_for_user_adult():
                            chatID = User_botgo(message.chat.id).get_ChatId_By_UserId()
                            bot.send_message(chatID, "В твоем городе появился турнир \n\n" + tournament)
                            log(message.chat.id, "new tournament sent", logging.INFO)

    except Exception as e:
        print(e)
    except AssertionError():
        print("!!!!!!! user has been blocked !!!!!!!")


def background():
    while True:
        Parsing.download_page("https://gofederation.ru/tournaments/", "html/current.html"),
        Parsing.compare("html/current.html", "html/old.html"),
        Parsing.copy_current_to_old("html/old.html", "html/current.html"),
        Parsing.main(),
        push_message(),
        Tournament_go.delete_old_tournaments(),
        now = datetime.datetime.now()

        if now.month == 12:
            nextyear = now.year + 1
            Parsing.download_page(f"https://gofederation.ru/tournaments?year={nextyear}", "html/current.html"),
            Parsing.compare("html/current.html", "html/old.html"),
            Parsing.copy_current_to_old("html/old.html", "html/current.html"),
            Parsing.main(),
            push_message()

        log(0, "stop cycle for 60 seconds", logging.INFO)
        time.sleep(60)


if __name__ == '__main__':
    t1 = Thread(target=background, args=())
    t1.start()
    bot.polling()
    Mysql.close_connect_db()
