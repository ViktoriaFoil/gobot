import queries_to_tables.database_query as query

def delete_old_tournaments(): #удаляет старые турниры, у которых дата старта меньше текущей даты
    name_query = "delete_old_tournaments"
    query_to_db = "DELETE FROM tournament_go WHERE t_start < current_date;"
    query.simple_type_without_return(name_query, query_to_db)


def all_tournaments_in_city(ID): #выполняет запрос на вывод пользователю всех туниров в его городе
    name_query = "all_tournaments_in_city"
    array = []
    query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go;"
    return query.query_with_ID(name_query, array, query_to_db, ID)


def get_adult_tournaments_in_city(chatID): #выполняет запрос на вывод пользователю всех взрослых туниров в его городе
    name_query = "get_adult_tournaments_in_city"
    array = []
    query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE is_child = 0;"
    return query.query_with_chatID(name_query, array, query_to_db, chatID)


def get_adult_tournaments_on_weekend(chatID): #выполняет запрос на вывод пользователю всех взрослых туниров в его городе на выходных
    name_query = "get_adult_tournaments_on_weekend"
    array = []
    query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE is_child = 0 AND DAYOFWEEK(t_start) IN (1,7);"
    return query.query_with_chatID(name_query, array, query_to_db, chatID)


def weekend_tournaments(chatID): #выполняет запрос на вывод пользователю турниров, которые состоятся на выходных 
    name_query = "weekend_tournaments"
    array = []
    query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE DAYOFWEEK(t_start) IN (1,7);"
    return query.query_with_chatID(name_query, array, query_to_db, chatID)


def get_new_tournaments(): #выполняет запрос на получения новых турниров
    name_query = "get_new_tournaments"  
    query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE date_time IN (SELECT MAX(date_time) FROM tournament_go);"
    return query.simple_type_with_return(name_query, query_to_db)


def tournaments_for_user(Id): #выполняет запрос на вывод турниров для рассылки
    name_query = "tournaments_for_user"
    array = []
    query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE 70 > (SELECT UNIX_TIMESTAMP(CURRENT_TIMESTAMP) - UNIX_TIMESTAMP(date_time));"
    return query.query_with_chatID(name_query, array, query_to_db, Id)


def tournaments_for_user_adult(Id): #выполняет запрос на вывод турниров для рассылки
    name_query = "tournaments_for_user_adult"
    array = []
    query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go WHERE is_child = 0 AND 70 > (SELECT UNIX_TIMESTAMP(CURRENT_TIMESTAMP) - UNIX_TIMESTAMP(date_time));"
    return query.query_with_chatID(name_query, array, query_to_db, Id)
    