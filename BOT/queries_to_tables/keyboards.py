import logging
from telebot import types
from BOT import log, mysql_dbconfig


class Keyboards:

    @staticmethod
    def get_keyboard(type_keyboard):
        try:
            keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mysql_dbconfig.cursor.execute(f"SELECT text_button FROM `keyboards` "
                                          f"WHERE type_keyboard = '{type_keyboard}';")
            keyboard = mysql_dbconfig.cursor.fetchall()
            for key in keyboard:
                keyb.add(key[0])
            return keyb
        except BaseException as e:
            log.log(0, "error get_key: " + str(e), logging.ERROR)
