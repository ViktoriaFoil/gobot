import logging
import locale
import datetime
from BOT import mysql_dbconfig, log
import BOT.bot as app


class Database_query:
    user_id: int
    chat_id: int

    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.user_id = app.User_botgo(chat_id).get_UserId_By_ChatId()

    @staticmethod
    def simple_type_without_return(name_query, query):
        try:
            mysql_dbconfig.cursor.execute(query)
            mysql_dbconfig.conn.commit()
        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def simple_type_with_return(name_query, query):
        try:
            mysql_dbconfig.cursor.execute(query)
            result = mysql_dbconfig.cursor.fetchall()
            mysql_dbconfig.conn.commit()
            return result
        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def simple_type_with_cycle(name_query, array, query):
        try:
            mysql_dbconfig.cursor.execute(query)
            result = mysql_dbconfig.cursor.fetchall()
            for item in result:
                array.append(item[0])
            mysql_dbconfig.conn.commit()
            return array
        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def simple_type_with_condition(name_query, query):
        try:
            line = ''
            mysql_dbconfig.cursor.execute(query)
            result = mysql_dbconfig.cursor.fetchall()
            if any(result):
                line = result[0][0]
            return str(line)
        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)

    def query_with_chatID(self, name_query, array, query):
        try:
            mysql_dbconfig.cursor.execute(query)
            result = mysql_dbconfig.cursor.fetchall()
            city_user = app.User_City(self.chat_id).get_cities_for_user()

            for city in city_user:
                for res in result:
                    ert = res[3]
                    if str(ert) == str(city):
                        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                        format_string = "%Y-%m-%d"
                        start = datetime.datetime.strptime(f"{res[0].year}-"
                                                           f"{res[0].month}-"
                                                           f"{res[0].day}",
                                                           format_string).strftime("%d %B %Y")
                        end = datetime.datetime.strptime(f"{res[1].year}-"
                                                         f"{res[1].month}-"
                                                         f"{res[1].day}",
                                                         format_string).strftime("%d %B %Y")
                        tournament = f"Начало: {start}\n" \
                                     f"Конец: {end}\n\n" \
                                     f"Название: {res[2]}\n\n" \
                                     f"Город: {app.Cities.get_CityName_By_Id(res[3])}\n\n" \
                                     f"Подробнее: {res[4]}\n"
                        array.append(tournament)
                        break

                   # mysql_dbconfig.conn.commit()

            return array

        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)

    @staticmethod
    def query_with_ID(name_query, array, query, chat_id):
        try:
            mysql_dbconfig.cursor.execute(query)
            result = mysql_dbconfig.cursor.fetchall()
            city_user = app.User_City(chat_id).get_cities_for_user()
            for res in result:
                if res[3] in city_user:
                    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                    format_string = "%Y-%m-%d"
                    start = datetime.datetime.strptime(f"{res[0].year}-"
                                                       f"{res[0].month}-"
                                                       f"{res[0].day}",
                                                       format_string).strftime("%d %B %Y")
                    end = datetime.datetime.strptime(f"{res[1].year}-"
                                                     f"{res[1].month}-"
                                                     f"{res[1].day}",
                                                     format_string).strftime("%d %B %Y")
                    tournament = f"Начало: {start}\n" \
                                 f"Конец: {end}\n\n" \
                                 f"Название: {res[2]}\n\n" \
                                 f"Город: {app.Cities.get_CityName_By_Id(res[3])}\n\n" \
                                 f"Подробнее: {res[4]}\n"
                    array.append(tournament)

            mysql_dbconfig.conn.commit()
            return array

        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)
