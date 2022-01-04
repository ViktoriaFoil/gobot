from APP.queries_to_tables.db_query import Database_query
from APP.queries_to_tables.user_botgo import User_botgo


class Cities:
    user_id: int
    chat_id: int

    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.user_id = User_botgo(chat_id).get_UserId_By_ChatId()

    def get_Cities_By_UserId(self):
        name_query = "getCitiesByUserId"
        array = []
        query_to_db = f"SELECT c.id FROM Cities as c " \
                      f"JOIN UserCity as uc ON uc.CityID = c.id " \
                      f"JOIN user_BotGo as u ON u.id = uc.UserID " \
                      f"WHERE uc.UserID = '{self.user_id}';"
        return Database_query.simple_type_with_cycle(name_query, array, query_to_db)

    def my_city(self):
        name_query = "my_city"
        array = []
        query_to_db = f"SELECT title FROM Cities as c " \
                      f"JOIN UserCity as uc ON uc.CityID = c.id " \
                      f"JOIN user_BotGo as u ON u.id = uc.UserID " \
                      f"WHERE u.chatID = '{self.chat_id}';"
        return Database_query.simple_type_with_cycle(name_query, array, query_to_db)

    @staticmethod
    def get_all_cities():
        name_query = "get_all_cities"
        array = []
        query_to_db = "SELECT title FROM `Cities`;"
        return Database_query.simple_type_with_cycle(name_query, array, query_to_db)

    @staticmethod
    def add_new_city(name):
        name_query = "add_new_city"
        query_to_db = f"INSERT INTO `Cities` (title) VALUES ('{name}')"
        Database_query.simple_type_without_return(name_query, query_to_db)

    @staticmethod
    def get_CityId_By_Name(name):
        name_query = "getCityIdByName"
        query_to_db = f"SELECT id FROM `Cities` Where title = '{name}';"
        return Database_query.simple_type_with_condition(name_query, query_to_db)

    @staticmethod
    def get_CityName_By_Id(city_id):
        name_query = "getCityNameById"
        query_to_db = f"SELECT title FROM `Cities` Where id = '{city_id}';"
        return Database_query.simple_type_with_condition(name_query, query_to_db)

    @staticmethod
    def get_UsersChat_By_CityId(city_id):
        name_query = "getUsersChatByCityId"
        array = []
        query_to_db = f"SELECT u.chatID FROM user_BotGo as u " \
                      f"JOIN UserCity as uc ON uc.UserID = u.id " \
                      f"JOIN Cities as c ON c.id = uc.CityID " \
                      f"WHERE c.id = '{city_id}';"
        return Database_query.simple_type_with_cycle(name_query, array, query_to_db)
