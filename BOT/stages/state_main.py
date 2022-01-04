import os
import telebot
from telebot import types
import logging
from BOT import log
import BOT.bot as app

token = os.getenv("BOT")
bot = telebot.TeleBot(token)


class State_main:

    @staticmethod
    def message_state_main(message):

        towns = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mainButton = app.Keyboards().get_keyboard("main")

        if message.text.lower() == "/start" or message.text.lower() == "приветствие":
            bot.send_message(message.chat.id, f"Здравствуй, {message.chat.first_name}", reply_markup=mainButton)
            log.log(message.chat.id, "send command /start", logging.INFO)
            return

        if message.text.lower() == "/my_city" or \
                message.text.lower() == "мой город" or \
                message.text.lower() == "мой город":
            log.log(message.chat.id, "send command /my_city", logging.INFO)
            for city in app.Cities(message.chat.id).my_city():
                bot.send_message(message.chat.id, city, reply_markup=mainButton)
            return

        if message.text.lower() == "/tournaments_in_my_city" or \
                message.text.lower() == "турниры в моем городе" or \
                message.text.lower() == "турниры в моем городе":
            if app.User_botgo(message.chat.id).is_user_child():
                tournaments = app.Tournament_go(message.chat.id).all_tournaments_in_city()
                if len(tournaments) == 0:
                    bot.send_message(message.chat.id, 'В твоем городе пока что нет запланированных турниров :(',
                                     reply_markup=mainButton)
                else:
                    for tournament in tournaments:
                        bot.send_message(message.chat.id, f"Турнир в твоем городе 🏆... \n\n {tournament}",
                                         reply_markup=mainButton)
                log.log(message.chat.id, "send command /tournaments_in_my_city, is child", logging.INFO)
            else:
                tournaments = app.Tournament_go(message.chat.id).get_adult_tournaments_in_city()
                log.log(message.chat.id, "send command /tournaments_in_my_city, is adult", logging.INFO)
                if len(tournaments) == 0:
                    bot.send_message(message.chat.id, 'В твоем городе пока что нет запланированных турниров :(',
                                     reply_markup=mainButton)
                else:
                    for tournament in tournaments:
                        bot.send_message(message.chat.id, f"Турнир в твоем городе 🏆... \n\n {tournament}",
                                         reply_markup=mainButton)
            return

        if message.text.lower() == "/message_to_developer" or \
                message.text.lower() == "сообщение автору" or \
                message.text.lower() == "сообщение автору":
            app.User_botgo(message.chat.id).query_change_state("message_to_developer")
            bot.send_message(message.chat.id, 'Напиши разработчику об ошибках, неисправностях, и тп. '
                                              'Отправь сюда сообщение, чтобы я отправил его разработчику',
                             reply_markup=types.ReplyKeyboardRemove())
            log.log(message.chat.id, "send command /message_to_developer, change of state", logging.INFO)
            return

        if message.text.lower() == "/change_city" or \
                message.text.lower() == "сменить город" or \
                message.text.lower() == "сменить город":
            app.User_City(message.chat.id).remove_city_for_user()
            app.User_botgo(message.chat.id).query_change_state("change_city")
            log.log(message.chat.id, "send command /change_city, change of state", logging.INFO)
            bot.send_message(message.chat.id, 'Я очистил твои города', reply_markup=towns)
            bot.send_message(message.chat.id, 'Нажми /start, выбирай новые города', reply_markup=towns)
            return

        if message.text.lower() == "/child_tournaments" or \
                message.text.lower() == "подписаться на детские турниры" or \
                message.text.lower() == "подписаться на детские турниры":
            for flag in app.User_botgo(message.chat.id).get_flag_is_child():
                if flag[0] == 0:
                    bot.send_message(message.chat.id, 'Ты подписался на рассылку детских турниров. '
                                                      'Это можно отменить командой /become_an_adult',
                                     reply_markup=mainButton)
                    app.User_botgo(message.chat.id).subscribe_to_child_change(1)
                    log.log(message.chat.id, "send command /child_tournaments, change of state", logging.INFO)
                if flag[0] == 1:
                    bot.send_message(message.chat.id, 'Ты уже подписан на детские турниры', reply_markup=mainButton)
                    log.log(message.chat.id, "send command /child_tournaments", logging.INFO)
            return

        if message.text.lower() == "/become_an_adult" or \
                message.text.lower() == "отписаться от детских турниров" or \
                message.text.lower() == "отписаться от детских турниров":
            for flag in app.User_botgo(message.chat.id).get_flag_is_child():
                if flag[0] == 0:
                    bot.send_message(message.chat.id, 'У тебя не было подписки на детские турниры',
                                     reply_markup=mainButton)
                    log.log(message.chat.id, "send command /become_an_adult", logging.INFO)
                if flag[0] == 1:
                    app.User_botgo(message.chat.id).subscribe_to_child_change(0)
                    bot.send_message(message.chat.id, 'Ты отписался от рассылки детских турниров',
                                     reply_markup=mainButton)
                    log.log(message.chat.id, "send command /become_an_adult,change of state", logging.INFO)
            return
        else:
            bot.send_message(message.chat.id, 'Я тебя не понимаю, напиши что-нибудь другое :(')
