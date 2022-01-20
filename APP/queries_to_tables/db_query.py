import logging

from config.mysql import cursor, conn
from logs.log import log
from telebot import types


class Database_query:

    @staticmethod
    def simple_type_without_return(name_query, query):
        try:
            cursor.execute(query)
            conn.commit()
        except Exception as e:
            log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def simple_type_with_return(name_query, query):
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()
            return result
        except Exception as e:
            log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def return_keys(name_query, query):
        try:
            keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            cursor.execute(query)
            keyboard = cursor.fetchall()
            for key in keyboard:
                keyb.add(key[0])
            return keyb
        except Exception as e:
            log(0, f"{name_query}: {e}", logging.ERROR)

    @staticmethod
    def simple_type_with_cycle(name_query, array, query):
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for item in result:
                array.append(item[0])
            conn.commit()
            return array
        except Exception as e:
            log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def simple_type_with_condition(name_query, query):
        try:
            line = ''
            cursor.execute(query)
            result = cursor.fetchall()
            if any(result):
                line = result[0][0]
            return str(line)
        except Exception as e:
            log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def return_true_or_false(name_query, query):
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            if result[0][0] == 0:
                return True
            else:
                return False
        except Exception as e:
            log(0, f"error {name_query} {e}", logging.ERROR)
