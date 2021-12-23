import logging
from BOT import log, mysql_dbconfig
import BOT.bot


class User_botgo:

    def get_flag_is_child(self, chatId):
        name_query = "get_flag_is_child"
        query_to_db = "SELECT is_child FROM user_BotGo WHERE id_User = '" + str(chatId) + "';"
        return BOT.bot.Database_query().simple_type_with_return(name_query, query_to_db)


    def selectState(self, chatID): #проверка состояния пользователя
        name_query = "selectState"
        query_to_db = "SELECT state_user FROM user_BotGo WHERE id_User = '" + str(chatID) + "';"
        return BOT.bot.Database_query().simple_type_with_condition(name_query, query_to_db)


    def getUserIdByChatId(self, chatId): # получить id пользователя из id телеграмма
        name_query = "getUserIdByChatId"
        query_to_db = "SELECT id FROM `user_BotGo` where id_User = '" + str(chatId) + "';"
        return BOT.bot.Database_query().simple_type_with_condition(name_query, query_to_db)


    def getChatIdByUserId(self, Id): # получить id телеграмма пользователя из id
        name_query = "getChatIdByUserId"
        query_to_db = "SELECT id_User FROM `user_BotGo` where id = '" + str(Id) + "';"
        return BOT.bot.Database_query().simple_type_with_condition(name_query, query_to_db)


    def query_change_state(self, state, chatID): #запрос на смену состояния пользователя
        name_query = "change_state"
        query_to_db = "UPDATE user_BotGo SET state_user = '" + str(state) + "' WHERE id_User = '" + str(chatID) + "';"
        BOT.bot.Database_query().simple_type_without_return(name_query, query_to_db)


    def subscribe_to_child_change(self, chatID, state): #подписка на детские турниры
        name_query = "subscribe_to_child_change"
        query_to_db = "UPDATE user_BotGo SET is_child = '" + str(state) + "' WHERE id_User = '" + str(chatID) + "'"
        BOT.bot.Database_query().simple_type_without_return(name_query, query_to_db)


    def check_exist_user(self, chatID): #проверка записи пользователя, чтобы не записывался один пользователь несколько раз
        query = "SELECT * FROM `user_BotGo` WHERE id_User='" + str(chatID) + "';"
        try:
            mysql_dbconfig.cursor.execute(query)
            if len(mysql_dbconfig.cursor.fetchall()) != 0:
                return True
            else:
                return False
        except BaseException as e:
            log.log(0, "error check_exist_user: " + str(e), logging.ERROR)


    def query_users(self, users): #выполнение запроса на заполнение данных о пользователе
        if User_botgo().check_exist_user(users[0]):
            return
        query = "INSERT INTO user_BotGo (id_User, first_name, last_name, username, state_user) VALUES( %s, %s, %s, %s, %s)"
        try:
            mysql_dbconfig.cursor.execute(query, users)
            mysql_dbconfig.conn.commit()
        except BaseException as e:
            log.log(0, "error query_users: " + str(e), logging.ERROR)


    def is_user_child(self, userId):
        try:
            mysql_dbconfig.cursor.execute("SELECT is_child FROM user_BotGo WHERE id = '" + str(userId) + "';")
            user = mysql_dbconfig.cursor.fetchall()
            return bool(user[0][0])

        except BaseException as e:
            log.log(0, "error is_user_child: " + str(e), logging.ERROR)