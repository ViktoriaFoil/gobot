
from queries_to_tables.db_query import Database_query


class Keyboards:

    @staticmethod
    def get_keyboard(type_keyboard):
        name_query = "get_keyboard"
        query_to_db = f"SELECT text_button FROM `keyboards` " \
                      f"WHERE type_keyboard = '{type_keyboard}';"
        array = Database_query.return_keys(name_query, query_to_db)
        return array

    @staticmethod
    def keyboard_with_tournament_names(user_id):
        
        name_query = "keyboard_with_tournament_names"
        query_to_db = f"SELECT t_name FROM tournament_go " \
                      f"WHERE CityID in (SELECT CityID FROM UserCity WHERE UserID = '{user_id}');"
        array = Database_query.return_keys(name_query, query_to_db)
        return array

    @staticmethod
    def keyboard_with_tournament_names_adult(user_id):
        name_query = "keyboard_with_tournament_names_adult"
        query_to_db = f"SELECT t_name FROM tournament_go " \
                      f"WHERE CityID in (SELECT CityID FROM UserCity WHERE UserID = '{user_id}') AND is_child = 0;"
        array = Database_query.return_keys(name_query, query_to_db)
        return array
