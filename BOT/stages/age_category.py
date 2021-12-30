import os
import telebot
import logging

from BOT import log
import BOT.bot as app

token = os.getenv("BOT")
bot = telebot.TeleBot(token)

class Age_category:

    def message_state_age_category(self, message):
        mainButton = app.Keyboards().get_keyboard("main")

        if message.text.lower() == "я ребенок, до 18 лет":
            app.User_botgo().subscribe_to_child_change(message.chat.id, 1)
            self.welcome(message.chat, mainButton)
            log.log(message.chat.id, "this user is child", logging.INFO)
        if message.text.lower() == "я взрослый":
            self.welcome(message.chat, mainButton)
            log.log(message.chat.id, "this user is adult", logging.INFO)


    def welcome(self, chat, mainButton):
        app.User_botgo().query_change_state("main", chat.id)
        bot.send_message(chat.id, 'Добро пожаловать 👋, ' + chat.first_name, reply_markup=mainButton)