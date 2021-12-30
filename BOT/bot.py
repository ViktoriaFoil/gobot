import os
import time
import datetime
import telebot
import logging
import log
import mysql_dbconfig
import BOT.main as main
from threading import Thread

from BOT.stages.massage_to_developer import Message_to_developer
from BOT.stages.state_main import State_main
from BOT.stages.city_selection_chenge import City_selection_chenge
from BOT.stages.age_category import Age_category

from BOT.queries_to_tables.database_query import Database_query
from BOT.queries_to_tables.cities import Cities
from BOT.queries_to_tables.keyboards import Keyboards
from BOT.queries_to_tables.children_categories import Children_categories
from BOT.queries_to_tables.user_botgo import User_botgo
from BOT.queries_to_tables.tournament_go import Tournament_go
from BOT.queries_to_tables.usercity import Usercity



token = os.getenv("BOT")
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])

def message(message):

    state = "city_selection"
    users = [
        message.chat.id,
        message.chat.first_name,
        message.chat.last_name,
        message.chat.username,
        state]

    User_botgo().query_users(users)

    SelectState = User_botgo().selectState(message.chat.id)

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
       State_main().message_state_main(message)
       return

    if SelectState == "message_to_developer" and message.text.lower() != "/message_to_developer" and message.text.lower() != "сообщение автору":
        Message_to_developer().mess_to_dev(message)
        return

#=======================================================================================================
#=======================================================================================================

def push_message(): 
    try:
        for new_tournaments in Tournament_go().get_new_tournaments(): # новые турниры
            for UserCity in Usercity().get_user_subscription_city(): # подписки на города пользователей
                if new_tournaments[3] == UserCity[1]: # если id города из новых турниров ровно id города в подписках, то
                    #userId = UserCity[0]
                    if(User_botgo().is_user_child(UserCity[0])): #если пользователь ребенок, отправлять все турниры
                        for tournament in Tournament_go().tournaments_for_user(UserCity[0]): #запрос строки на отправку турнира
                            chatID = User_botgo().getChatIdByUserId(UserCity[0])
                            bot.send_message(chatID, "В твоем городе появился турнир \n\n" + tournament) #отправить
                            log.log(message.chat.id, "a new children's tournament has been sent", logging.INFO)
                    else: # иначе пользователь взрослый
                        for tournament in Tournament_go().tournaments_for_user_adult(UserCity[0]): #запрос строки на отправку турнира
                            chatID = User_botgo().getChatIdByUserId(UserCity[0])
                            bot.send_message(chatID, "В твоем городе появился турнир \n\n" + tournament) #отправить
                            log.log(message.chat.id, "new tournament sent", logging.INFO)
    except Exception as e:
            print(e)
    except AssertionError():
            print( "!!!!!!! user has been blocked !!!!!!!" )


def background():
    while True:
        main.download_page("https://gofederation.ru/tournaments/", "BOT/current.html"),  # скачивание актуальной версии турниров
        main.compare("BOT/current.html", "BOT/old.html"),  # сравнение
        main.copy_current_to_old("BOT/old.html", "BOT/current.html"),  # замена старого на новое
        main.main(),  # запись новых турниров
        push_message(),  # уведомление пользователей о новых турнирах
        Tournament_go().delete_old_tournaments(),  # удаление устаревших по дате турниров из основной таблицы

        now = datetime.datetime.now()
        if now.month == 12:
            nextyear = now.year + 1
            main.download_page(f"https://gofederation.ru/tournaments?year={nextyear}", "BOT/current.html"),
            main.compare("BOT/current.html", "BOT/old.html"),  # сравнение
            main.copy_current_to_old("BOT/old.html", "BOT/current.html"),  # замена старого на новое
            main.main(),  # запись новых турниров
            push_message()  # уведомление пользователей о новых турнирах
        
        log.log(0, "stop cycle for 60 seconds", logging.INFO)
        time.sleep(60)


if __name__ == '__main__':
    t1 = Thread(target=background, args=())
    t1.start()
    bot.polling(none_stop=True)
    mysql_dbconfig.close_connect_db()