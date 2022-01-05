import os
import telebot
from telebot import types
import logging

from logs.log import log
from queries_to_tables.cities import Cities
from queries_to_tables.keyboards import Keyboards
from queries_to_tables.tournament_go import Tournament_go
from queries_to_tables.user_botgo import User_botgo
from queries_to_tables.usercity import User_City

token = os.getenv("BOT")
bot = telebot.TeleBot(token)


class State_main:

    @staticmethod
    def message_state_main(message):

        towns = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mainButton = Keyboards.get_keyboard("main")

        if message.text.lower() == "/start" or message.text.lower() == "приветствие":
            bot.send_message(message.chat.id, f"Здравствуй, {message.chat.first_name}", reply_markup=mainButton)
            log(message.chat.id, "send command /start", logging.INFO)
            return

        if message.text.lower() == "/my_city" or \
                message.text.lower() == "мой город" or \
                message.text.lower() == "мой город":
            log(message.chat.id, "send command /my_city", logging.INFO)
            for city in Cities(message.chat.id).my_city():
                bot.send_message(message.chat.id, city, reply_markup=mainButton)
            return

        if message.text.lower() == "/tournaments_in_my_city" or \
                message.text.lower() == "турниры в моем городе" or \
                message.text.lower() == "турниры в моем городе":
            if User_botgo(message.chat.id).is_user_child():
                tournaments = Tournament_go(message.chat.id).all_tournaments_in_city()
                if tournaments is None:
                    bot.send_message(message.chat.id, 'В твоем городе пока что нет запланированных турниров :(',
                                     reply_markup=mainButton)
                else:
                    for tournament in tournaments:
                        bot.send_message(message.chat.id, f"Турнир в твоем городе 🏆... \n\n {tournament}",
                                         reply_markup=mainButton)
                log(message.chat.id, "send command /tournaments_in_my_city, is child", logging.INFO)
            else:
                tournaments = Tournament_go(message.chat.id).get_adult_tournaments_in_city()
                log(message.chat.id, "send command /tournaments_in_my_city, is adult", logging.INFO)
                if tournaments is None:
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
            User_botgo(message.chat.id).query_change_state("message_to_developer")
            bot.send_message(message.chat.id, 'Напиши разработчику об ошибках, неисправностях, и тп. '
                                              'Отправь сюда сообщение, чтобы я отправил его разработчику',
                             reply_markup=types.ReplyKeyboardRemove())
            log(message.chat.id, "send command /message_to_developer, change of state", logging.INFO)
            return

        if message.text.lower() == "/change_city" or \
                message.text.lower() == "сменить город" or \
                message.text.lower() == "сменить город":
            User_City(message.chat.id).remove_city_for_user()
            User_botgo(message.chat.id).query_change_state("change_city")
            log(message.chat.id, "send command /change_city, change of state", logging.INFO)
            bot.send_message(message.chat.id, 'Я очистил твои города', reply_markup=towns)
            bot.send_message(message.chat.id, 'Нажми /start, выбирай новые города', reply_markup=towns)
            return

        if message.text.lower() == "/child_tournaments" or \
                message.text.lower() == "подписаться на детские турниры" or \
                message.text.lower() == "подписаться на детские турниры":
            for flag in User_botgo(message.chat.id).get_flag_is_child():
                if flag[0] == 0:
                    bot.send_message(message.chat.id, 'Ты подписался на рассылку детских турниров. '
                                                      'Это можно отменить командой /become_an_adult',
                                     reply_markup=mainButton)
                    User_botgo(message.chat.id).subscribe_to_child_change(1)
                    log(message.chat.id, "send command /child_tournaments, change of state", logging.INFO)
                if flag[0] == 1:
                    bot.send_message(message.chat.id, 'Ты уже подписан на детские турниры', reply_markup=mainButton)
                    log(message.chat.id, "send command /child_tournaments", logging.INFO)
            return

        if message.text.lower() == "/become_an_adult" or \
                message.text.lower() == "отписаться от детских турниров" or \
                message.text.lower() == "отписаться от детских турниров":
            for flag in User_botgo(message.chat.id).get_flag_is_child():
                if flag[0] == 0:
                    bot.send_message(message.chat.id, 'У тебя не было подписки на детские турниры',
                                     reply_markup=mainButton)
                    log(message.chat.id, "send command /become_an_adult", logging.INFO)
                if flag[0] == 1:
                    User_botgo(message.chat.id).subscribe_to_child_change(0)
                    bot.send_message(message.chat.id, 'Ты отписался от рассылки детских турниров',
                                     reply_markup=mainButton)
                    log(message.chat.id, "send command /become_an_adult,change of state", logging.INFO)
            return
        else:
            bot.send_message(message.chat.id, 'Я тебя не понимаю, напиши что-нибудь другое :(')
