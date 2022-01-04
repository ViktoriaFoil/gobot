import BOT.bot as app


class User_City:
    user_id: int
    chat_id: int

    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.user_id = app.User_botgo(chat_id).get_UserId_By_ChatId()

    def get_cities_for_user(self):
        name_query = "get_cities_for_user"
        array = []
        query_to_db = f"SELECT CityID FROM UserCity WHERE UserID = {self.user_id}"
        return app.Database_query.simple_type_with_cycle(name_query, array, query_to_db)

    def add_city(self, city):
        city_id = app.Cities.get_CityId_By_Name(city)
        name_query = "add_city"
        query_to_db = f"INSERT INTO UserCity (UserID, CityID) VALUES ('{self.user_id}', '{city_id}');"
        app.Database_query.simple_type_without_return(name_query, query_to_db)

    def remove_city_for_user(self):
        name_query = "remove_city_for_user"
        query_to_db = f"DELETE FROM UserCity WHERE UserID = " \
                      f"(select id from user_BotGo WHERE chatID = '{self.chat_id}');"
        app.Database_query.simple_type_without_return(name_query, query_to_db)

    def get_user_subscription_city(self):
        name_query = "get_user_subscription_city"
        query_to_db = f"SELECT CityID FROM UserCity WHERE UserID = " \
                      f"'(select id from user_BotGo WHERE chatID = '{self.chat_id}');"
        return app.Database_query.simple_type_with_return(name_query, query_to_db)
