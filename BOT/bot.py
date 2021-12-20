import os
import time
from threading import Thread
import telebot
from telebot import types
import main
import logging
import mysql_dbconfig as db
import log
import queries_to_tables.cities as cities
import queries_to_tables.user_botgo as user_botgo
import queries_to_tables.tournament_go as tournament_go
import queries_to_tables.usercity as usercity
import queries_to_tables.keyboards as keyboards

token = os.getenv("BOT")
bot = telebot.TeleBot(token)
state = "city_selection"
global listCity
listCity = []


@bot.message_handler(content_types=['text'])

def message(message):

    towns = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mainButton = keyboards.get_keyboard("main")
    age = keyboards.get_keyboard("age")
    navigation = keyboards.get_keyboard("navigation")

    users = [
        message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, "city_selection"]

    user_botgo.query_users(users)
    SelectState = user_botgo.selectState(message.chat.id)

#=======================================================================================================
#ИСПРАВНО

    if SelectState == "city_selection":
        all_city = sorted(set(cities.get_all_cities()) - set(listCity))
        for city in all_city:
            towns.add(types.KeyboardButton(city))


        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Привет, выбери города 🏘, в которых турниры актуальны для тебя 😉', reply_markup=towns)
            log.log(message.chat.id, "send command /start", logging.INFO)


        if message.html_text in all_city:
            usercity.add_city(message.chat.id, message.html_text)
            listCity.append(message.html_text)
            bot.send_message(message.chat.id, 'Если хочешь выбрать еще города, нажми ДАЛЕЕ, если нет, то нажми СТОП', reply_markup=navigation)
            log.log(message.chat.id, "user selects a city", logging.INFO)


        if message.html_text == 'далее':
            bot.send_message(message.chat.id, 'Выбери город', reply_markup=towns)
            log.log(message.chat.id, "the user selects an additional city", logging.INFO)


        if message.html_text == 'стоп':
            user_botgo.query_change_state("age_category", message.chat.id)
            SelectState = user_botgo.selectState(message.chat.id)
            bot.send_message(message.chat.id, 'Выбери свою категорию. Это нужно, чтобы я фильтровал для тебя турниры. В категории я ребенок, присылаюся все турниры. В категории я взрослый, только взрослые турниры.', reply_markup=age)
            log.log(message.chat.id, "the user has selected all the cities that interest him, switched to the age selection state", logging.INFO)
            listCity.clear()

#=======================================================================================================
#ИСПРАВНО

    if SelectState == "change_city":
        all_city = sorted(set(cities.get_all_cities()) - set(listCity))
        for city in all_city:
            towns.add(types.KeyboardButton(city))

        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Выбери города 😉', reply_markup=towns)
            log.log(message.chat.id, "user changes cities", logging.INFO)


        if message.html_text in all_city:
            usercity.add_city(message.chat.id, message.html_text)
            listCity.append(message.html_text)
            bot.send_message(message.chat.id, 'Если хочешь выбрать еще города, нажми ДАЛЕЕ, если нет, то нажми СТОП', reply_markup=navigation)


        if message.html_text == 'далее':
            bot.send_message(message.chat.id, 'Выбери город', reply_markup=towns)


        if message.html_text == 'стоп':
            user_botgo.query_change_state('main', message.chat.id)
            SelectState = user_botgo.selectState(message.chat.id)
            bot.send_message(message.chat.id, 'Смена городов произведена успешно', reply_markup=mainButton)
            log.log(message.chat.id, "the user has successfully changed cities", logging.INFO)
            listCity.clear()
            return


#=======================================================================================================
#ИСПРАВНО

    if SelectState == "age_category":
        if message.text.lower() == "я ребенок, до 18 лет":
            user_botgo.subscribe_to_child_change(message.chat.id, 1)
            welcome(message.chat, mainButton)
            log.log(message.chat.id, "this user is child", logging.INFO)
        if message.text.lower() == "я взрослый":
            welcome(message.chat, mainButton)
            log.log(message.chat.id, "this user is adult", logging.INFO)
        return

#=======================================================================================================
 #ИСПРАВНО

    if SelectState == "main":
        if message.text.lower() == "/start" or message.text.lower() == "приветствие":
            bot.send_message(message.chat.id, 'Здравствуй, ' + message.chat.first_name, reply_markup=mainButton)
            log.log(message.chat.id, "send command /start", logging.INFO)
            return


        if message.text.lower() == "/my_city" or message.text.lower() == "мой город" or message.text.lower() == "мой город":
            log.log(message.chat.id, "send command /my_city", logging.INFO)
            for city in cities.my_city(message.chat.id):
                bot.send_message(message.chat.id, city, reply_markup=mainButton)
            return

        # переделать запрос
        if message.text.lower() == "/tournaments_in_my_city" or message.text.lower() == "турниры в моем городе" or message.text.lower() == "турниры в моем городе":
            userID = user_botgo.getUserIdByChatId(message.chat.id)
            if user_botgo.is_user_child(userID):
                tournaments = tournament_go.all_tournaments_in_city(userID)
                if len(tournaments) == 0:
                    bot.send_message(message.chat.id, 'В твоем городе пока что нет запланированных турниров :(',reply_markup=mainButton)
                else:
                    for tournament in tournaments:
                        bot.send_message(message.chat.id, 'Турнир в твоем городе 🏆... \n\n' + tournament,reply_markup=mainButton)
                log.log(message.chat.id, "send command /tournaments_in_my_city, is child", logging.INFO)
            else:
                tournaments = tournament_go.get_adult_tournaments_in_city(userID)
                log.log(message.chat.id, "send command /tournaments_in_my_city, is adult", logging.INFO)
                if len(tournaments) == 0:
                    bot.send_message(message.chat.id, 'В твоем городе пока что нет запланированных турниров :(', reply_markup=mainButton)
                else:
                    for tournament in tournaments:
                        bot.send_message(message.chat.id, 'Турнир в твоем городе 🏆... \n\n' + tournament, reply_markup=mainButton)
            return


        if message.text.lower() == "/message_to_developer" or message.text.lower() == "сообщение автору" or message.text.lower() == "сообщение автору":
            user_botgo.query_change_state("message_to_developer", message.chat.id)
            SelectState = user_botgo.selectState(message.chat.id)
            bot.send_message(message.chat.id, 'Напиши разработчику об ошибках, неисправностях, и тп. Отправь сюда сообщение, чтобы я отправил его разработчику', reply_markup=types.ReplyKeyboardRemove())
            log.log(message.chat.id, "send command /message_to_developer, change of state", logging.INFO)
            return


        if message.text.lower() == "/change_city" or message.text.lower() == "сменить город" or message.text.lower() == "сменить город":
            usercity.remove_city_for_user(message.chat.id)
            user_botgo.query_change_state("change_city", message.chat.id)
            SelectState = user_botgo.selectState(message.chat.id)
            log.log(message.chat.id, "send command /change_city, change of state", logging.INFO)
            bot.send_message(message.chat.id, 'Я очистил твои города', reply_markup=towns)
            bot.send_message(message.chat.id, 'Нажми /start, выбирай новые города', reply_markup=towns)
            return


        if message.text.lower() == "/child_tournaments" or message.text.lower() == "подписаться на детские турниры" or message.text.lower() == "подписаться на детские турниры":
            for flag in user_botgo.get_flag_is_child(message.chat.id):
                if flag[0] == 0:
                    bot.send_message(message.chat.id, 'Ты подписался на рассылку детских турниров. Это можно отменить командой /become_an_adult', reply_markup=mainButton)
                    user_botgo.subscribe_to_child_change(message.chat.id, 1)
                    log.log(message.chat.id, "send command /child_tournaments, change of state", logging.INFO)
                if flag[0] == 1:
                    bot.send_message(message.chat.id, 'Ты уже подписан на детские турниры', reply_markup=mainButton)
                    log.log(message.chat.id, "send command /child_tournaments", logging.INFO)
            return


        if message.text.lower() == "/become_an_adult" or message.text.lower() == "отписаться от детских турниров" or message.text.lower() == "отписаться от детских турниров":
            for flag in user_botgo.get_flag_is_child(message.chat.id):
                if flag[0] == 0:
                    bot.send_message(message.chat.id, 'У тебя не было подписки на детские турниры', reply_markup=mainButton)
                    log.log(message.chat.id, "send command /become_an_adult", logging.INFO)
                if flag[0] == 1:
                    user_botgo.subscribe_to_child_change(message.chat.id, 0)
                    bot.send_message(message.chat.id, 'Ты отписался от рассылки детских турниров', reply_markup=mainButton)
                    log.log(message.chat.id, "send command /become_an_adult,change of state", logging.INFO)
            return
        else:
            bot.send_message(message.chat.id, 'Я тебя не понимаю, напиши что-нибудь другое :(')


#=======================================================================================================
  #ИСАПРАВНО

    if SelectState == "message_to_developer" and message.text.lower() != "/message_to_developer" and message.text.lower() != "сообщение автору":
        bot.send_message(925936432, f"Сообщение от: \n{message.chat.id}\n{message.html_text}")
        bot.send_message(message.chat.id, "Отправил")
        user_botgo.query_change_state("main", message.chat.id)
        log.log(message.chat.id, "sent a letter to the developer, change of state", logging.INFO)
        bot.send_message(message.chat.id, 'Если хочешь еще раз написать разработчику, напиши команду /message_to_developer', reply_markup=mainButton)

#=======================================================================================================

def push_message(): #ПРОВЕРИТЬ
    try:
        for new_tournaments in tournament_go.get_new_tournaments(): # новые турниры
            for UserCity in usercity.get_user_subscription_city(): # подписки на города пользователей
                if new_tournaments[3] == UserCity[1]: # если id города из новых турниров ровно id города в подписках, то
                    #userId = UserCity[0]
                    if(user_botgo.is_user_child(UserCity[0])): #если пользователь ребенок, отправлять все турниры
                        for tournament in tournament_go.tournaments_for_user(UserCity[0]): #запрос строки на отправку турнира
                            chatID = user_botgo.getChatIdByUserId(UserCity[0])
                            bot.send_message(chatID, "В твоем городе появился турнир \n\n" + tournament) #отправить
                            log.log(message.chat.id, "a new children's tournament has been sent", logging.INFO)
                    else: # иначе пользователь взрослый
                        for tournament in tournament_go.tournaments_for_user_adult(UserCity[0]): #запрос строки на отправку турнира
                            chatID = user_botgo.getChatIdByUserId(UserCity[0])
                            bot.send_message(chatID, "В твоем городе появился турнир \n\n" + tournament) #отправить
                            log.log(message.chat.id, "new tournament sent", logging.INFO)
    except Exception as e:
            print(e)
    except AssertionError():
            print( "!!!!!!! user has been blocked !!!!!!!" )


def welcome(chat, mainButton):
    user_botgo.query_change_state("main", chat.id)
    SelectState = user_botgo.selectState(chat.id)
    bot.send_message(chat.id, 'Добро пожаловать 👋, ' + chat.first_name, reply_markup=mainButton)


def background():
    while True:
        main.download_page("https://gofederation.ru/tournaments/", "current.html"),  # скачивание актуальной версии турниров
        main.compare("current.html", "old.html"),  # сравнение
        main.copy_current_to_old("old.html", "current.html"),  # замена старого на новое
        main.main(),  # запись новых турниров
        push_message(),  # уведомление пользователей о новых турнирах
        tournament_go.delete_old_tournaments(),  # удаление устаревших по дате турниров из основной таблицы
        log.log(0, "stop cycle for 60 seconds", logging.INFO)

        time.sleep(60)


if __name__ == '__main__':
    t1 = Thread(target=background, args=())
    t1.start()
    bot.polling(none_stop=True)
    db.close_connect_db()