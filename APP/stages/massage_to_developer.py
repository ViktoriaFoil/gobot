import os
import telebot
import logging

from logs.log import log
from queries_to_tables.keyboards import Keyboards
from queries_to_tables.user_botgo import User_botgo

token = os.getenv("BOT")
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
class Message_to_developer:

    @staticmethod
    def mess_to_dev(message):
        mainButton = Keyboards.get_keyboard("main")

        bot.send_message(925936432, f"Сообщение от: \n{message.chat.id}\n{message.html_text}")
        bot.send_message(message.chat.id, "Отправил")
        User_botgo(message.chat.id).query_change_state("main")
        log(message.chat.id, "sent a letter to the developer, change of state", logging.INFO)
        bot.send_message(message.chat.id, 'Если хочешь еще раз написать разработчику, '
                                          'напиши команду /message_to_developer', reply_markup=mainButton)
