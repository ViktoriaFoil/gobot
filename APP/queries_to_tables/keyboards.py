import logging
from telebot import types

from APP.config.mysql import Mysql
from APP.logs.log import log


class Keyboards:

    @staticmethod
    def get_keyboard(type_keyboard):
        try:
            keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            Mysql.cursor.execute(f"SELECT text_button FROM `keyboards` "
                                          f"WHERE type_keyboard = '{type_keyboard}';")
            keyboard = Mysql.cursor.fetchall()
            for key in keyboard:
                keyb.add(key[0])
            return keyb
        except BaseException as e:
            log(0, "error get_key: " + str(e), logging.ERROR)
