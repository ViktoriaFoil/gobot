import queries_to_tables.database_query as query

def getCitiesByUserId(userId):
    name_query = "getCitiesByUserId" 
    array = []
    query_to_db = "SELECT c.id FROM Cities as c JOIN UserCity as uc ON uc.CityID = c.id JOIN user_BotGo as u ON u.id = uc.UserID WHERE uc.UserID = '" + str(userId) + "';"
    return query.simple_type_with_cycle(name_query, array, query_to_db)


def my_city(chatID): #запрос пользователя на город\города на которые он подписан
    name_query = "my_city"
    array = []
    query_to_db = "SELECT title FROM Cities as c JOIN UserCity as uc ON uc.CityID = c.id JOIN user_BotGo as u ON u.id = uc.UserID WHERE u.id_User = '" + str(chatID) + "';"
    return query.simple_type_with_cycle(name_query, array, query_to_db)


def get_all_cities(): #запрос на получение списка городов
    name_query = "get_all_cities"
    array = []
    query_to_db = "SELECT title FROM `Cities`;"
    return query.simple_type_with_cycle(name_query, array, query_to_db)


def getCityIdByName(name): #получить id города из его названия
    name_query = "getCityIdByName"
    query_to_db = "SELECT id FROM `Cities` Where title = '" + str(name) + "';"
    return query.simple_type_with_condition(name_query, query_to_db)


def getCityNameById(id): # получить название города из его id
    name_query = "getCityNameById"
    query_to_db = "SELECT title FROM `Cities` Where id = '" + str(id) + "';"
    return query.simple_type_with_condition(name_query, query_to_db)


def getUsersChatByCityId(CityId):
    name_query = "getUsersChatByCityId"
    array = []
    query_to_db = "SELECT u.id_User FROM user_BotGo as u JOIN UserCity as uc ON uc.UserID = u.id JOIN Cities as c ON c.id = uc.CityID WHERE c.id = '" + str(CityId) + "'"
    return query.simple_type_with_cycle(name_query, array, query_to_db)