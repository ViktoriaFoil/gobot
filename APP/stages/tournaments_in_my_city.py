import os

import telebot

from queries_to_tables.user_botgo import User_botgo
from queries_to_tables.keyboards import Keyboards
from queries_to_tables.tournament_go import Tournament_go

token = os.getenv("BOT")
bot = telebot.TeleBot(token)


class Tournament_in_my_city:

    @staticmethod
    def in_my_city(chat_id, message):
        mainButton = Keyboards.get_keyboard("main")
        user_id = User_botgo(message.chat.id).get_UserId_By_ChatId()
        all_names = Tournament_go(message.chat.id).all_tour_names()
        if User_botgo(chat_id).is_user_child():
            name_tour = Keyboards.keyboard_with_tournament_names(user_id)
            text = message.html_text
            if message.html_text in all_names:
                tournaments = Tournament_go(chat_id).specified_name(text)
                for tournament in tournaments:
                    bot.send_message(chat_id, f"Турнир по вызову имени \n\n{tournament}",
                                     reply_markup=mainButton)
                User_botgo(chat_id).query_change_state("main")
            else:
                bot.send_message(chat_id, "Нет такого названия в моем списке турниров, выбери другое",
                                 reply_markup=name_tour)
        else:
            name_tour = Keyboards.keyboard_with_tournament_names_adult(user_id)
            text = message.html_text
            if message.html_text in all_names:
                tournaments = Tournament_go(chat_id).specified_name_adult(text)
                for tournament in tournaments:
                    bot.send_message(chat_id, f"Турнир по вызову имени \n\n{tournament}",
                                     reply_markup=mainButton)
                User_botgo(chat_id).query_change_state("main")
            else:
                bot.send_message(chat_id, "Нет такого названия в моем списке турниров, выбери другое",
                                 reply_markup=name_tour)