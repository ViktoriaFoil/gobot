import logging
from telebot import types
from BOT import log, mysql_dbconfig

class Keyboards:

    def get_keyboard(self, type): # получает текст кнопок
        try:
            keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mysql_dbconfig.cursor.execute("SELECT text_button FROM `keyboards` WHERE type_keyboard = '" + type + "';")
            keyboard = mysql_dbconfig.cursor.fetchall()
            for key in keyboard:
                keyb.add(key[0])
            return keyb
        except BaseException as e:
            log.log(0, "error get_key: " + str(e), logging.ERROR)

