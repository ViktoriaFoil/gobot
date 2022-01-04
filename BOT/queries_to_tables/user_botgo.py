import logging
from BOT import log, mysql_dbconfig
import BOT.bot as app


class User_botgo:
    user_id: int
    chat_id: int

    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.user_id = self.get_UserId_By_ChatId()

    def get_flag_is_child(self):
        name_query = "get_flag_is_child"
        query_to_db = f"SELECT is_child FROM user_BotGo WHERE chatID = '{self.chat_id}';"
        return app.Database_query.simple_type_with_return(name_query, query_to_db)

    def selectState(self):
        name_query = "selectState"
        query_to_db = f"SELECT state_user FROM user_BotGo WHERE chatID = {self.chat_id};"
        return app.Database_query.simple_type_with_condition(name_query, query_to_db)

    def get_UserId_By_ChatId(self):
        name_query = "get_UserId_By_ChatId"
        query_to_db = f"SELECT id FROM `user_BotGo` where chatID = '{self.chat_id}';"
        return app.Database_query.simple_type_with_condition(name_query, query_to_db)

    def get_ChatId_By_UserId(self):
        name_query = "getChatIdByUserId"
        query_to_db = f"SELECT chatID FROM `user_BotGo` where id = '{self.user_id}';"
        return app.Database_query.simple_type_with_condition(name_query, query_to_db)

    def query_change_state(self, state):
        name_query = "change_state"
        query_to_db = f"UPDATE user_BotGo SET state_user = '{state}' " \
                      f"WHERE chatID = '{self.chat_id}';"
        app.Database_query.simple_type_without_return(name_query, query_to_db)

    def subscribe_to_child_change(self, state):
        name_query = "subscribe_to_child_change"
        query_to_db = f"UPDATE user_BotGo SET is_child = '{state}' " \
                      f"WHERE chatID = '{self.chat_id}';"
        app.Database_query.simple_type_without_return(name_query, query_to_db)

    @staticmethod
    def check_exist_user(chat_id):
        query = f"SELECT * FROM `user_BotGo` WHERE chatID='{chat_id}';"
        try:
            mysql_dbconfig.cursor.execute(query)
            if len(mysql_dbconfig.cursor.fetchall()) != 0:
                return True
            else:
                return False
        except BaseException as e:
            log.log(0, f"error check_exist_user: '{e}'", logging.ERROR)

    @staticmethod
    def query_users(users):
        if User_botgo.check_exist_user(users.chat_id):
            return
        query = f"INSERT INTO user_BotGo (chatID, first_name, last_name, username, state_user) " \
                f"VALUES( {users.chat_id}, " \
                f"'{users.first_name}', " \
                f"'{users.last_name}', " \
                f"'{users.username}', " \
                f"'{users.state}')"
        try:
            mysql_dbconfig.cursor.execute(query, users)
            mysql_dbconfig.conn.commit()
        except BaseException as e:
            log.log(0, f"error query_users: '{e}'", logging.ERROR)

    def is_user_child(self):
        try:
            mysql_dbconfig.cursor.execute(f"SELECT is_child FROM user_BotGo WHERE id = '{self.user_id}';")
            user = mysql_dbconfig.cursor.fetchall()
            return bool(user[0][0])

        except BaseException as e:
            log.log(0, f"error is_user_child: '{e}'", logging.ERROR)
