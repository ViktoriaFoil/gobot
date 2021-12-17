import BOT.log as log
import logging
import locale
import BOT.queries_to_tables.cities as cities
import BOT.queries_to_tables.user_botgo as user_botgo
import BOT.mysql_dbconfig as db
import datetime


def simple_type_without_return(name_query, query):
    try:
        db.cursor.execute(query)
        db.conn.commit()
    except BaseException as e:
        log.log(0, f"error {name_query} {e}", logging.ERROR)


def simple_type_with_return(name_query, query):
    try:
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        db.conn.commit()
        return result
    except BaseException as e:
        log.log(0, f"error {name_query} {e}", logging.ERROR)


def simple_type_with_cycle(name_query, array, query):
    try:
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        for item in result:
            array.append(item[0])
        db.conn.commit()
        return array
    except BaseException as e:
        log.log(0, f"error {name_query} {e}", logging.ERROR)


def simple_type_with_condition(name_query, query):
    try:
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        if any(result):
            line = result[0][0]
        return str(line)
    except BaseException as e: #local variable 'line' referenced before assignment
        log.log(0, f"error {name_query} {e}", logging.ERROR)


def query_with_chatID(name_query, array, query, chatID):
    try:
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        userId = user_botgo.getUserIdByChatId(chatID)
        city_user = cities.getCitiesByUserId(userId)
        for res in result:
            if str(res[3]) in city_user:
                locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                format_string = "%Y-%m-%d"
                start = datetime.datetime.strptime(str(res[0]), format_string).strftime("%d %B %Y")
                end = datetime.datetime.strptime(str(res[1]), format_string).strftime("%d %B %Y")
                tournament = f"Начало: {start}\n"
                tournament += f"Конец: {end}\n\n"
                tournament += f"Название: {res[2]}\n\n"
                tournament += f"Город: {cities.getCityNameById(res[3])}\n\n"
                tournament += f"Подробнее: {res[4]}\n"
                array.append(tournament)

        db.conn.commit()
        return array

    except BaseException as e:
        log.log(0, f"error {name_query} {e}", logging.ERROR)


def query_with_ID(name_query, array, query, Id):
    try:
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        city_user = cities.getCitiesByUserId(Id)
        for res in result:
            if res[3] in city_user:
                locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                format_string = "%Y-%m-%d"
                start = datetime.datetime.strptime(f"{res[0].year}-{res[0].month}-{res[0].day}", format_string).strftime("%d %B %Y")
                end = datetime.datetime.strptime(f"{res[1].year}-{res[1].month}-{res[1].day}", format_string).strftime("%d %B %Y")
                tournament = f"Начало: {start}\n"
                tournament += f"Конец: {end}\n\n"
                tournament += f"Название: {res[2]}\n\n"
                tournament += f"Город: {cities.getCityNameById(res[3])}\n\n"
                tournament += f"Подробнее: {res[4]}\n"
                array.append(tournament)

        db.conn.commit()
        return array

    except BaseException as e:
        log.log(0, f"error {name_query} {e}", logging.ERROR)
