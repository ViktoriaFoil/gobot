import log as log
import logging
import mysql_dbconfig as db
import queries_to_tables.database_query as query


def get_flag_is_child(chatId):
    name_query = "get_flag_is_child"
    query_to_db = "SELECT is_child FROM user_BotGo WHERE id_User = '" + str(chatId) + "';"
    return query.simple_type_with_return(name_query, query_to_db)


def selectState(chatID): #проверка состояния пользователя
    name_query = "selectState"
    query_to_db = "SELECT state_user FROM user_BotGo WHERE id_User = '" + str(chatID) + "';"
    return query.simple_type_with_condition(name_query, query_to_db)


def getUserIdByChatId(chatId): # получить id пользователя из id телеграмма
    name_query = "getUserIdByChatId"
    query_to_db = "SELECT id FROM `user_BotGo` where id_User = '" + str(chatId) + "';"
    return query.simple_type_with_condition(name_query, query_to_db)


def getChatIdByUserId(Id): # получить id телеграмма пользователя из id
    name_query = "getChatIdByUserId"
    query_to_db = "SELECT id_User FROM `user_BotGo` where id = '" + str(Id) + "';"
    return query.simple_type_with_condition(name_query, query_to_db)


def query_change_state(state, chatID): #запрос на смену состояния пользователя
    name_query = "change_state"
    query_to_db = "UPDATE user_BotGo SET state_user = '" + str(state) + "' WHERE id_User = '" + str(chatID) + "';"
    query.simple_type_without_return(name_query, query_to_db)


def subscribe_to_child_change(chatID, state): #подписка на детские турниры
    name_query = "subscribe_to_child_change"
    query_to_db = "UPDATE user_BotGo SET is_child = '" + str(state) + "' WHERE id_User = '" + str(chatID) + "'"
    query.simple_type_without_return(name_query, query_to_db)


def check_exist_user(chatID): #проверка записи пользователя, чтобы не записывался один пользователь несколько раз
    query = "SELECT * FROM `user_BotGo` WHERE id_User='" + str(chatID) + "';"
    try:
        db.cursor.execute(query)
        if len(db.cursor.fetchall()) != 0:
            return True
        else:
            return False
    except BaseException as e:
        log.log(0, "error check_exist_user: " + str(e), logging.ERROR)


def query_users(users): #выполнение запроса на заполнение данных о пользователе
    if check_exist_user(users[0]):
        return
    query = "INSERT INTO user_BotGo (id_User, first_name, last_name, username, state_user) VALUES( %s, %s, %s, %s, %s)"
    try:
        db.cursor.execute(query, users)
        db.conn.commit()
    except BaseException as e:
        log.log(0, "error query_users: " + str(e), logging.ERROR)


def is_user_child(userId):
    try:
        db.cursor.execute("SELECT is_child FROM user_BotGo WHERE id = '" + str(userId) + "';")
        user = db.cursor.fetchall()
        return bool(user[0][0])

    except BaseException as e:
        log.log(0, "error is_user_child: " + str(e), logging.ERROR)