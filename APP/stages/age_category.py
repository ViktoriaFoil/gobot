import os
import telebot
import logging

from APP.logs.log import log
from APP.queries_to_tables.keyboards import Keyboards
from APP.queries_to_tables.user_botgo import User_botgo

token = os.getenv("BOT")
bot = telebot.TeleBot(token)


class Age_category:

    @staticmethod
    def message_state_age_category(message):
        mainButton = Keyboards.get_keyboard("main")

        if message.text.lower() == "я ребенок, до 18 лет":
            User_botgo(message.chat.id).subscribe_to_child_change(1)
            Age_category.welcome(message.chat.id, mainButton)
            log(message.chat.id, "this user is child", logging.INFO)
        if message.text.lower() == "я взрослый":
            Age_category.welcome(message.chat.id, mainButton)
            log(message.chat.id, "this user is adult", logging.INFO)

    @staticmethod
    def welcome(chat_id, mainButton):
        User_botgo(chat_id).query_change_state("main")
        bot.send_message(chat_id, 'Добро пожаловать 👋 ' , reply_markup=mainButton)
