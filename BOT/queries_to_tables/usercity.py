import BOT.bot as app

class Usercity:

    def add_city(self, chatID, city): #запрос на добавления пользователю города, в которых он хочет получать информацию о новых турнирах
        userId = app.User_botgo().getUserIdByChatId(chatID)
        cityId = app.Cities().getCityIdByName(city)
        name_query = "add_city"
        query_to_db = "INSERT INTO UserCity (UserID, CityID) VALUES ('" + str(userId) + "', '" + str(cityId) + "');"
        app.Database_query().simple_type_without_return(name_query, query_to_db)


    def remove_city_for_user(self, chatId):
        name_query = "remove_city_for_user"
        query_to_db = "DELETE FROM UserCity WHERE UserID = (select id from user_BotGo WHERE id_User = '" + str(chatId) + "');"
        app.Database_query().simple_type_without_return(name_query, query_to_db)


    def get_user_subscription_city(self):
        name_query = "get_user_subscription_city"
        query_to_db = "SELECT UserID, CityID FROM UserCity;"
        return app.Database_query().simple_type_with_return(name_query, query_to_db)