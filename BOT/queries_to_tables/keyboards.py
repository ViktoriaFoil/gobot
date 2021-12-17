import BOT.log as log
import logging
import BOT.mysql_dbconfig as db
from telebot import types


def get_keyboard(type): # получает текст кнопок
    try:
        keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        db.cursor.execute("SELECT text_button FROM `keyboards` WHERE type_keyboard = '" + str(type) + "';")
        keyboard = db.cursor.fetchall()
        for key in keyboard:
            keyb.add(key[0])
        return keyb
    except BaseException as e:
        log.log(0, "error get_key: " + str(e), logging.ERROR)

