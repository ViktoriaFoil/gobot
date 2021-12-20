import queries_to_tables.user_botgo as user_botgo
import queries_to_tables.cities as cities
import queries_to_tables.database_query as query

def add_city(chatID, city): #запрос на добавления пользователю города, в которых он хочет получать информацию о новых турнирах
    userId = user_botgo.getUserIdByChatId(chatID)
    cityId = cities.getCityIdByName(city)
    name_query = "add_city"
    query_to_db = "INSERT INTO UserCity (UserID, CityID) VALUES ('" + str(userId) + "', '" + str(cityId) + "');"
    query.simple_type_without_return(name_query, query_to_db)


def remove_city_for_user(chatId):
    name_query = "remove_city_for_user"
    query_to_db = "DELETE FROM UserCity WHERE UserID = (select id from user_BotGo WHERE id_User = '" + str(chatId) + "');"
    query.simple_type_without_return(name_query, query_to_db)


def get_user_subscription_city():
    name_query = "get_user_subscription_city"
    query_to_db = "SELECT UserID, CityID FROM UserCity;"
    return query.simple_type_with_return(name_query, query_to_db)