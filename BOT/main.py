import requests
import os
from bs4 import BeautifulSoup
from datetime import date 
import tournament
import datetime
import locale
import bot
import logging
import mysql_dbconfig as db
from log import log
from datetime import datetime   #Библиотеки

def date(): #функция для вывода сегодняшней даты            
    today = datetime.now().date()
    return today

def download_page(url, name):  #функция для скачивания актуальной версии турниров по ссылке
    try:
        r = requests.get(url)
        bot.log(0, "download page " + url, logging.INFO)
        with open(name, 'w') as output_file:
            output_file.write(r.text.replace("&nbsp;-&nbsp;", ""))
            bot.log(0, "save url to " + name, logging.INFO)
        r.close()
    except Exception as e:
        bot.log(0, "error download page: " + str(e), logging.ERROR)

def record_set(page): #функция, которая удаляет все переносы строк в файле (делает одну строку)
    try:
        with open(page, 'r') as f:
            content = f.read().replace('\n', '')
            soup = BeautifulSoup(content, 'lxml')
            result_set = set()
            for item in soup.find_all("tr"):
                result_set.add(str(item))
            return result_set
    except Exception as e:
        bot.log(0, "error record set: " + str(e), logging.ERROR)

def compare(current_page, old_page): #функция для сравнения старой версии турниров с новой, различия записываются в файл difference
    try:
        old_records = record_set(old_page)
        bot.log(0, "record set: " + old_page, logging.INFO)
        current_records = record_set(current_page)
        bot.log(0, "record set " + current_page, logging.INFO)
        open('difference.html', 'w').close()
        new_records = []

        with open('difference.html', 'a') as f: # проверка отличий
            for line in current_records:
                if line not in old_records:
                    new_records.append(line)
            f.writelines(new_records)
            bot.log(0, "save to difference.html", logging.INFO)
    except Exception as e:
        bot.log(0, "error compare: " + str(e), logging.ERROR)

def copy_current_to_old(old_page, current_page): # функция для перезаписи старой версии файла
    try:
        with open(current_page, 'r') as current:
            with open(old_page, 'w') as old:
                old.write(current.read())
                old.close()
                current.close()
                bot.log(0, "information overwritten", logging.INFO)
    except Exception as e:
        bot.log(0, "error copy current to old: " + str(e), logging.ERROR)

def check_exist_file(name): 
    if not os.path.isfile(name):
        with open(name, 'w'): pass

def insert_tournament(tournaments): #добавляет турниры в базу данных

    for tour in tournaments:
        query = "INSERT INTO tournament_go (t_start, t_end, t_name, CityID, link, is_child) VALUES(%s, %s, %s, %s, %s, %s)"

        try:
            cityId = int(getCityIdByName(tour.city))
            db.cursor.execute(query, [tour.start, tour.end, tour.name, cityId, tour.link, tour.flag])
            db.conn.commit()
        except BaseException as e:
            bot.log(0, "error insert tournament: " + str(e), logging.ERROR)

def main(): #связывает 2 функции insert_tournament и getText
    try:
        tournaments = getText()
        insert_tournament(tournaments)
        bot.log(0, "successful entry of new tournaments into the database", logging.INFO)
    except BaseException as e:
        bot.log(0, "error main: " + str(e), logging.ERROR)

def getText(): #получает текст для вставки новых турниров в базу данных
    html = open('difference.html')
    root = BeautifulSoup(html, 'lxml')
    tr = root.select('tr')
    tournaments = []

    for t in tr:
        td = t.select('td')
        a = t.select('a')
        tour = tournament.Tournament()
        try:
            for i in td:
           
                if "padding-right" in str(i):
                    text_date = i.text.replace("\xa0-\xa0", "")
                    format_string = "%d.%m.%Y"
                    t_start = datetime.strptime(text_date, format_string).strftime("%Y-%m-%d")
                    tour.setStart(t_start)
                    continue

                if "padding-left" in str(i):
                    text_date = i.text
                    format_string = "%d.%m.%Y"
                    t_end = datetime.strptime(text_date, format_string).strftime("%Y-%m-%d")
                    tour.setEnd(t_end)
                    continue

                if "tournament" in str(i):
                    t_name = i.text.replace(" (", ", ").replace(")", "")
                    is_child = 0
                    for categories in set_children_categories():
                        if categories in t_name:
                            is_child = 1
                            tour.setFlag(is_child)
                    tour.setFlag(is_child)
                    tour.setName(t_name)
                    continue

                link = "https://gofederation.ru" + str(a[0].attrs['href'])
                tour.setLink(link)
            
                city = i.text #.replace("Сервер", "").replace(", КГС", "").replace(", KGS", "").replace(", OGS", "").replace("(КГС)", "").replace("(ОГС)", "").replace(", ОГС", "").replace("OGS", "ОГС").replace("KGS", "КГС").replace(", GoQuest", "").replace(" (GoQuest)", "")
                tour.setCity(city)

                tournaments.append(tour)
                return tournaments
        except BaseException as e:
            bot.log(0, "error getText: " + str(e), logging.ERROR)


def set_children_categories(): #запрос на получение списка категорий

    children_categories = []
    try:
        db.cursor.execute("SELECT categories FROM `children_categories`;")
        records = db.cursor.fetchall()
        for categories in records:
            children_categories.append(categories[0])
        return children_categories

    except BaseException as e:
        bot.log(0, "error set children categories: " + str(e), logging.ERROR)


def delete_old_tournaments(): #удаляет старые турниры, у которых дата старта меньше текущей даты
    try:
        date_var = str(date())
        sql = "DELETE FROM tournament_go WHERE DATE(t_start) < DATE(%s);"
        params = [date_var]
        db.cursor.execute(sql, params)
        db.conn.commit()
        bot.log(0, "successful deletion of old tournaments", logging.INFO)
        
    except BaseException as e:
        bot.log(0, "error delete old tournaments: " + str(e), logging.ERROR)

def all_tournaments_in_city(chatID): #выполняет запрос на вывод пользователю всех туниров в его городе
    all_tournaments = []
    try:
        db.cursor.execute("SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go;")
        result = db.cursor.fetchall()

        userId = getUserIdByChatId(chatID)
        city_user = getCitiesByUserId(userId)

        for res in result:
            if str(res[3]) in city_user:
                locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                format_string = "%Y-%m-%d"
                start = datetime.strptime(str(res[0]), format_string).strftime("%d %B %Y")
                end = datetime.strptime(str(res[1]), format_string).strftime("%d %B %Y")
                tournament = "Начало: " + str(start) + "\n"
                tournament += "Конец: " + str(end) + "\n\n"
                tournament += "Название: " + res[2] + "\n\n"
                tournament += "Город: " + getCityNameById(res[3]) + "\n\n"
                tournament += "Подробнее: " + res[4] + "\n"
                all_tournaments.append(tournament)

        db.conn.commit()
        return all_tournaments

    except BaseException as e:
        bot.log(0, "error all tournaments in city: " + str(e), logging.ERROR)


def get_adult_tournaments_in_city(chatID): #выполняет запрос на вывод пользователю всех туниров в его городе
    all_tournaments = []
    try:
        db.cursor.execute("SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE is_child = 0;")
        result = db.cursor.fetchall()

        userId = getUserIdByChatId(chatID)
        city_user = getCitiesByUserId(userId)

        for res in result:
            if str(res[3]) in city_user:
                locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                format_string = "%Y-%m-%d"
                start = datetime.strptime(str(res[0]), format_string).strftime("%d %B %Y")
                end = datetime.strptime(str(res[1]), format_string).strftime("%d %B %Y")
                tournament = "Начало: " + str(start) + "\n"
                tournament += "Конец: " + str(end) + "\n\n"
                tournament += "Название: " + res[2] + "\n\n"
                tournament += "Город: " + getCityNameById(res[3]) + "\n\n"
                tournament += "Подробнее: " + res[4] + "\n"
                all_tournaments.append(tournament)

        db.conn.commit()
        return all_tournaments

    except BaseException as e:
        bot.log(0, "error get_adult_tournaments_in_city: " + str(e), logging.ERROR)


def get_adult_tournaments_on_weekend(chatID): #выполняет запрос на вывод пользователю всех туниров в его городе на выходных
    all_tournaments = []
    try:
        db.cursor.execute("SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE is_child = 0 AND DAYOFWEEK(t_start) IN (1,7);")
        result = db.cursor.fetchall()

        userId = getUserIdByChatId(chatID)
        city_user = getCitiesByUserId(userId)

        for res in result:
            if str(res[3]) in city_user:
                locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                format_string = "%Y-%m-%d"
                start = datetime.strptime(str(res[0]), format_string).strftime("%d %B %Y")
                end = datetime.strptime(str(res[1]), format_string).strftime("%d %B %Y")
                tournament = "Начало: " + str(start) + "\n"
                tournament += "Конец: " + str(end) + "\n\n"
                tournament += "Название: " + res[2] + "\n\n"
                tournament += "Город: " + getCityNameById(res[3]) + "\n\n"
                tournament += "Подробнее: " + res[4] + "\n"
                all_tournaments.append(tournament)

        db.conn.commit()
        return all_tournaments

    except BaseException as e:
        bot.log(0, "error get_adult_tournaments_on_weekend: " + str(e), logging.ERROR)


def getCitiesByUserId(userId):
        try:
            ids = []
            db.cursor.execute("SELECT c.id FROM Cities as c JOIN UserCity as uc ON uc.CityID = c.id JOIN user_BotGo as u ON u.id = uc.UserID WHERE uc.UserID = '" + str(userId) + "';")
            records = db.cursor.fetchall()

            for id in records:
                ids.append(id[0])
            db.conn.commit()

            return ids

        except BaseException as e:
            bot.log(0, "error getCitiesByUserId: " + str(e), logging.ERROR)



def get_flag_is_child(chatId):
    try:
        db.cursor.execute("SELECT is_child FROM user_BotGo WHERE id_User = '" + str(chatId) + "';")
        result = db.cursor.fetchall()
        db.conn.commit()
        return result

    except BaseException as e:
        bot.log(0, "error get_flag_is_child: " + str(e), logging.ERROR)


def weekend_tournaments(chatID): #выполняет запрос на вывод пользователю турниров, которые состоятся на выходных текущей недели

    try:
        db.cursor.execute("SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE DAYOFWEEK(t_start) IN (1,7);")
        result = db.cursor.fetchall()

        userId = getUserIdByChatId(chatID)
        city_user = getCitiesByUserId(userId)

        week_tournaments = []

        for res in result:
            if str(res[3]) in city_user:
                locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                format_string = "%Y-%m-%d"
                start = datetime.strptime(str(res[0]), format_string).strftime("%d %B %Y")
                end = datetime.strptime(str(res[1]), format_string).strftime("%d %B %Y")
                tournament = "Начало: " + str(start) + "\n"
                tournament += "Конец: " + str(end) + "\n\n"
                tournament += "Название: " + res[2] + "\n\n"
                tournament += "Город: " + getCityNameById(res[3]) + "\n\n"
                tournament += "Подробнее: " + res[4] + "\n"
                week_tournaments.append(tournament)

        db.conn.commit()
        return week_tournaments


    except BaseException as e:
        bot.log(0, "error weekend_tournaments: " + str(e), logging.ERROR)


def check_exist_user(chatID): #проверка записи пользователя, чтобы не записывался один пользователь несколько раз

    query = "SELECT * FROM `user_BotGo` WHERE id_User='" + str(chatID) + "';"
    try:
        db.cursor.execute(query)

        if len(db.cursor.fetchall()) != 0:
            return True
        else:
            return False

    except BaseException as e:
        bot.log(0, "error check_exist_user: " + str(e), logging.ERROR)

def query_users(users): #выполнение запроса на заполнение данных о пользователе

    if check_exist_user(users[0]):
        return

    query = "INSERT INTO user_BotGo (id_User, first_name, last_name, username, state_user) VALUES( %s, %s, %s, %s, %s)"
    try:
        db.cursor.execute(query, users)
        db.conn.commit()
    except BaseException as e:
        bot.log(0, "error query_users: " + str(e), logging.ERROR)

def query_change_state(state, chatID): #запрос на смену состояния пользователя

    query = "UPDATE user_BotGo SET state_user = '" + state + "' WHERE id_User = '" + str(chatID) + "'"
    try:
        db.cursor.execute(query, state)
        db.conn.commit()
    except BaseException as e:
        bot.log(0, "error query_change_state: " + str(e), logging.ERROR)

def subscribe_to_child_change(chatID, state): #подписка на детские турниры

    query = "UPDATE user_BotGo SET is_child = '" + str(state) + "' WHERE id_User = '" + str(chatID) + "'"
    try:
        db.cursor.execute(query, state)
        db.conn.commit()
    except BaseException as e:
        bot.log(0, "error subscribe_to_child_change: " + str(e), logging.ERROR)

def add_city(chatID, city): #запрос на добавления пользователю города, в которых он хочет получать информацию о новых турнирах

    try:
        userId = getUserIdByChatId(chatID)
        cityId = getCityIdByName(city)
        db.cursor.execute("INSERT INTO UserCity (UserID, CityID) VALUES ('" + str(userId) + "', '" + str(cityId) + "');")
        db.conn.commit()
    except BaseException as e:
        bot.log(0, "error add_city: " + str(e), logging.ERROR)

def selectState(chatID): #проверка состояния пользователя

    SelectState = ""
    try:
        db.cursor.execute("SELECT state_user FROM user_BotGo WHERE id_User = '" + str(chatID) + "'")
        records = db.cursor.fetchall()
        SelectState = records[0][0]
        return SelectState
    except BaseException as e:
        bot.log(0, "error selectState: " + str(e), logging.ERROR)


def my_city(chatID): #запрос пользователя на город\города на которые он подписан

    my_city = ""
    try:
        db.cursor.execute("SELECT title FROM Cities as c JOIN UserCity as uc ON uc.CityID = c.id JOIN user_BotGo as u ON u.id = uc.UserID WHERE u.id_User = '" + str(chatID) + "'")
        records = db.cursor.fetchall()
        my_city = []
        for item in records:
            my_city.append(item[0])
        return my_city

    except BaseException as e:
        bot.log(0, "error my_city: " + str(e), logging.ERROR)


def get_all_cities(): #запрос на получение списка городов

    all_city = []
    try:
        db.cursor.execute("SELECT title FROM `Cities`;")
        records = db.cursor.fetchall()
        for city in records:
            all_city.append(city[0])

        return all_city


    except BaseException as e:
        bot.log(0, "error get_all_cities: " + str(e), logging.ERROR)


def getCityIdByName(name): #получить id города из его названия

    cityId = 0
    try:
        db.cursor.execute("SELECT id FROM `Cities` Where title = '" + str(name) + "';")
        records = db.cursor.fetchall()

        if any(records):
            cityId = records[0][0]

        return str(cityId)

    except BaseException as e:
        bot.log(0, "error getCityIdByName: " + str(e), logging.ERROR)


def getCityNameById(id): # получить название города из его id

    cityName = ''
    try:
        db.cursor.execute("SELECT title FROM `Cities` Where id = '" + str(id) + "';")
        records = db.cursor.fetchall()
        if any(records):
            cityName = records[0][0]

        return str(cityName)

    except BaseException as e:
        bot.log(0, "error getCityNameById: " + str(e), logging.ERROR)


def getUserIdByChatId(chatId): # получить id пользователя из id телеграмма 

    userId = 0
    try:
        db.cursor.execute("SELECT id FROM `user_BotGo` where id_User = '" + str(chatId) + "';")
        records = db.cursor.fetchall()
        if any(records):
            userId = records[0][0]

        return userId

    except BaseException as e:
        bot.log(0, "error getUserIdByChatId: " + str(e), logging.ERROR)


def getChatIdByUserId(Id): # получить id телеграмма пользователя из id  

    try:
        db.cursor.execute("SELECT id_User FROM `user_BotGo` where id = '" + str(Id) + "';")
        records = db.cursor.fetchall()
        if any(records):
            Id = records[0][0]

        return Id

    except BaseException as e:
        bot.log(0, "error getChatIdByUserId: " + str(e), logging.ERROR)


def getUsersChatByCityId(CityId): #

    chats = []
    try:
        db.cursor.execute("SELECT u.id_User FROM user_BotGo as u JOIN UserCity as uc ON uc.UserID = u.id JOIN Cities as c ON c.id = uc.CityID WHERE c.id = '" + str(CityId) + "'")
        records = db.cursor.fetchall()
        for item in records:
            chats.append(item[0])

        return chats

    except BaseException as e:
        bot.log(0, "error getUsersChatByCityId: " + str(e), logging.ERROR)


def remove_city_for_user(chatId):
    try:
        db.cursor.execute("DELETE FROM UserCity WHERE UserID = (select id from user_BotGo WHERE id_User = '" + str(chatId) + "');")
        db.conn.commit()
        
    except BaseException as e:
        bot.log(0, "error remove_city_for_user: " + str(e), logging.ERROR)

def is_user_child(userId):
    try:
        db.cursor.execute("SELECT is_child FROM user_BotGo WHERE id = '" + str(userId) + "';")
        user = db.cursor.fetchall()[0]
        return bool(user[0])
        
    except BaseException as e:
        bot.log(0, "error is_user_child: " + str(e), logging.ERROR)

def get_new_tournaments(): #выполняет запрос на получения новых турниров
    try:
        db.cursor.execute("SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE date_time IN (SELECT MAX(date_time) FROM tournament_go);")
        result = db.cursor.fetchall()

        db.conn.commit()
        return result

    except BaseException as e:
        bot.log(0, "error get_new_tournaments: " + str(e), logging.ERROR)


def get_user_subscription_city():
    try:
        db.cursor.execute("SELECT UserID, CityID FROM UserCity;")
        result = db.cursor.fetchall()

        db.conn.commit()
        return result

    except BaseException as e:
        bot.log(0, "error get_user_subscription_city: " + str(e), logging.ERROR)


def tournaments_for_user(Id): #выполняет запрос на вывод турниров для рассылки
    all_tournaments = []
    try:
        db.cursor.execute("SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE 310 > (SELECT UNIX_TIMESTAMP(CURRENT_TIMESTAMP) - UNIX_TIMESTAMP(date_time));")
        result = db.cursor.fetchall()

        city_user = getCitiesByUserId(Id)

        for res in result:
            if str(res[3]) in city_user:
                text_date_start = res[0]
                text_date_end = res[1]
                format_string = "%Y-%m-%d"
                locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                start = datetime.strptime(str(text_date_start), str(format_string)).strftime("%d %B %Y")
                end = datetime.strptime(str(text_date_end), str(format_string)).strftime("%d %B %Y")
                tournament = "Начало: " + str(start) + "\n"
                tournament += "Конец: " + str(end) + "\n\n"
                tournament += "Название: " + res[2] + "\n\n"
                tournament += "Город: " + getCityNameById(res[3]) + "\n\n"
                tournament += "Подробнее: " + res[4] + "\n"
                all_tournaments.append(tournament)

        db.conn.commit()
        return all_tournaments

    except BaseException as e:
        bot.log(0, "error tournaments_for_user: " + str(e), logging.ERROR)



def tournaments_for_user_adult(Id): #выполняет запрос на вывод турниров для рассылки
    all_tournaments = []
    try:
        db.cursor.execute("SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE is_child = 0 AND 310 > (SELECT UNIX_TIMESTAMP(CURRENT_TIMESTAMP) - UNIX_TIMESTAMP(date_time));")

        result = db.cursor.fetchall()

        city_user = getCitiesByUserId(Id)
        all_tournaments = []

        for res in result:
            if res[3] in city_user:
                text_date_start = res[0]
                text_date_end = res[1]
                format_string = "%Y-%m-%d"
                locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                start = datetime.strptime(str(text_date_start), str(format_string)).strftime("%d %B %Y")
                end = datetime.strptime(str(text_date_end), str(format_string)).strftime("%d %B %Y")
                tournament = "Начало: " + str(start) + "\n"
                tournament += "Конец: " + str(end) + "\n\n"
                tournament += "Название: " + res[2] + "\n\n"
                tournament += "Город: " + getCityNameById(res[3]) + "\n\n"
                tournament += "Подробнее: " + res[4] + "\n"
                all_tournaments.append(tournament)

        db.conn.commit()

        return all_tournaments

    except BaseException as e:
        bot.log(0, "error tournaments_for_user_adult: " + str(e), logging.ERROR)


    