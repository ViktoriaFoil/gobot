import logging
import locale
import datetime
from BOT import mysql_dbconfig, log
import BOT.bot


class Database_query:

    def simple_type_without_return(self, name_query, query):
        try:
            mysql_dbconfig.cursor.execute(query)
            mysql_dbconfig.conn.commit()
        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)


    def simple_type_with_return(self, name_query, query):
        try:
            mysql_dbconfig.cursor.execute(query)
            result = mysql_dbconfig.cursor.fetchall()
            mysql_dbconfig.conn.commit()
            return result
        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)


    def simple_type_with_cycle(self, name_query, array, query):
        try:
            mysql_dbconfig.cursor.execute(query)
            result = mysql_dbconfig.cursor.fetchall()
            for item in result:
                array.append(item[0])
            mysql_dbconfig.conn.commit()
            return array
        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)


    def simple_type_with_condition(self, name_query, query):
        try:
            line = ''
            mysql_dbconfig.cursor.execute(query)
            result = mysql_dbconfig.cursor.fetchall()
            if any(result):
                line = result[0][0]
            return str(line)
        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)


    def query_with_chatID(self, name_query, array, query, chatID):
        try:
            mysql_dbconfig.cursor.execute(query)
            result = mysql_dbconfig.cursor.fetchall()
            userId = BOT.bot.User_botgo().getUserIdByChatId(chatID)
            city_user = BOT.bot.Cities().getCitiesByUserId(userId)
            for res in result:
                if str(res[3]) in city_user:
                    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                    format_string = "%Y-%m-%d"
                    start = datetime.datetime.strptime(str(res[0]), format_string).strftime("%d %B %Y")
                    end = datetime.datetime.strptime(str(res[1]), format_string).strftime("%d %B %Y")
                    tournament = f"Начало: {start}\n"
                    tournament += f"Конец: {end}\n\n"
                    tournament += f"Название: {res[2]}\n\n"
                    tournament += f"Город: {BOT.bot.Cities().getCityNameById(res[3])}\n\n"
                    tournament += f"Подробнее: {res[4]}\n"
                    array.append(tournament)

            mysql_dbconfig.conn.commit()
            return array

        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)


    def query_with_ID(self, name_query, array, query, Id):
        try:
            mysql_dbconfig.cursor.execute(query)
            result = mysql_dbconfig.cursor.fetchall()
            city_user = BOT.bot.Cities().getCitiesByUserId(Id)
            for res in result:
                if res[3] in city_user:
                    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                    format_string = "%Y-%m-%d"
                    start = datetime.datetime.strptime(f"{res[0].year}-{res[0].month}-{res[0].day}", format_string).strftime("%d %B %Y")
                    end = datetime.datetime.strptime(f"{res[1].year}-{res[1].month}-{res[1].day}", format_string).strftime("%d %B %Y")
                    tournament = f"Начало: {start}\n"
                    tournament += f"Конец: {end}\n\n"
                    tournament += f"Название: {res[2]}\n\n"
                    tournament += f"Город: {BOT.bot.Cities().getCityNameById(res[3])}\n\n"
                    tournament += f"Подробнее: {res[4]}\n"
                    array.append(tournament)

            mysql_dbconfig.conn.commit()
            return array

        except BaseException as e:
            log.log(0, f"error {name_query} {e}", logging.ERROR)
