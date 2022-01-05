import logging

from config.mysql import cursor, conn
from logs.log import log
from objects.send_tournament import SendTournament
from queries_to_tables.cities import Cities
from queries_to_tables.db_query import Database_query
from queries_to_tables.user_botgo import User_botgo


class Tournament_go:
    user_id: int
    chat_id: int

    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.user_id = User_botgo(chat_id).get_UserId_By_ChatId()

    @staticmethod
    def insert_tournament(tournaments):
        for tour in tournaments:
            query = "INSERT INTO tournament_go (t_start, t_end, t_name, CityID, link, is_child) " \
                    "VALUES(%s, %s, %s, %s, %s, %s)"

            try:
                city_id = int(Cities.get_CityId_By_Name(tour.city))
                cursor.execute(query, [tour.start, tour.end, tour.name, city_id, tour.link, tour.flag])
                conn.commit()
            except BaseException as e:
                log(0, "error insert tournament: " + str(e), logging.ERROR)

    @staticmethod
    def delete_old_tournaments():
        name_query = "delete_old_tournaments"
        query_to_db = "DELETE FROM tournament_go WHERE t_start < current_date;"
        Database_query.simple_type_without_return(name_query, query_to_db)

    def all_tournaments_in_city(self):
        name_query = "all_tournaments_in_city"
        array = []
        query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go;"
        array = SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)

        if array is None:
            return []
        else:
            return array

    def get_adult_tournaments_in_city(self):
        name_query = "get_adult_tournaments_in_city"
        array = []
        query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      "WHERE is_child = 0;"
        array = SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)

        if array is None:
            return []
        else:
            return array

    @staticmethod
    def get_adult_tournaments_on_weekend(chat_id):
        name_query = "get_adult_tournaments_on_weekend"
        array = []
        query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      "WHERE is_child = 0 AND DAYOFWEEK(t_start) IN (1,7);"
        return SendTournament.send_tournament(chat_id, name_query, array, query_to_db)

    @staticmethod
    def weekend_tournaments(chat_id):
        name_query = "weekend_tournaments"
        array = []
        query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      "WHERE DAYOFWEEK(t_start) IN (1,7);"
        return SendTournament.send_tournament(chat_id, name_query, array, query_to_db)

    @staticmethod
    def get_new_tournaments():
        name_query = "get_new_tournaments"
        query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      "WHERE date_time IN (SELECT MAX(date_time) FROM tournament_go);"
        return Database_query.simple_type_with_return(name_query, query_to_db)

    def tournaments_for_user(self):
        name_query = "tournaments_for_user"
        array = []
        query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      "WHERE 70 > (SELECT UNIX_TIMESTAMP(CURRENT_TIMESTAMP) - UNIX_TIMESTAMP(date_time));"
        return SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)

    def tournaments_for_user_adult(self):
        name_query = "tournaments_for_user_adult"
        array = []
        query_to_db = f"SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      f"WHERE is_child = 0 " \
                      f"AND 70 > (SELECT UNIX_TIMESTAMP(CURRENT_TIMESTAMP) - UNIX_TIMESTAMP(date_time));"
        return SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)
    