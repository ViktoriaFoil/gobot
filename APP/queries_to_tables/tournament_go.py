import logging
import os

from objects.send_tournament import SendTournament
from queries_to_tables.db_query import Database_query
from queries_to_tables.user_botgo import User_botgo

from main import Parsing

from logs.log import log


class Tournament_go:
    user_id: int
    chat_id: int

    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.user_id = User_botgo(chat_id).get_UserId_By_ChatId()

    def specified_name(self, text):
        name_query = "specified_name"
        array = []
        query_to_db = f"SELECT t_start, t_end, t_name, CityID, link, is_child " \
                      f"FROM tournament_go WHERE t_name = '{text}';"
        array = SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)
        return array

    def specified_name_adult(self, text):
        name_query = "specified_name_adult"
        array = []
        query_to_db = f"SELECT t_start, t_end, t_name, CityID, link, is_child " \
                      f"FROM tournament_go WHERE t_name = '{text}' AND is_child = 0;"
        array = SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)
        return array

    @staticmethod
    def all_tournaments_without_details():
        name_query = "all_tournaments_without_details"
        all_without_details = "SELECT link FROM tournament_go WHERE details = 'not_exist';"
        array = Database_query.simple_type_with_return(name_query, all_without_details)
        return array

    def all_tour_names_adult(self):
        name_query = "all_tour_names"
        query_to_db = f"SELECT t_name FROM tournament_go " \
                      f"WHERE CityID in (SELECT CityID FROM UserCity WHERE UserID = '{self.user_id}') AND is_child = 0;"
        array = []
        return Database_query.simple_type_with_cycle(name_query, array, query_to_db)

    def all_tour_names(self):
        name_query = "all_tour_names"
        query_to_db = f"SELECT t_name FROM tournament_go " \
                      f"WHERE CityID in (SELECT CityID FROM UserCity WHERE UserID = '{self.user_id}');"
        array = []
        return Database_query.simple_type_with_cycle(name_query, array, query_to_db)

    @staticmethod
    def number_of_entries():
        name_query = "number of entries"
        query_to_db = "SELECT COUNT(*) FROM tournament_go;"
        return Database_query.return_true_or_false(name_query, query_to_db)

    @staticmethod
    def update_tournament_details():
        query_to_db = f"UPDATE tournament_go SET details = 'exist' WHERE details = 'for_mailing';"
        name_query = "update_tournament_details"
        Database_query.simple_type_without_return(name_query, query_to_db)

    @staticmethod
    def change_new_to_notified():
        name_query = "change_new_to_notified"
        query_to_db = "UPDATE tournament_go SET is_new = 'no' WHERE is_new = 'yes';"
        Database_query.simple_type_without_return(name_query, query_to_db)

    @staticmethod
    def delete_old_tournaments():
        name_query = "delete_old_tournaments"
        query_to_db = "DELETE FROM tournament_go WHERE t_start < current_date;"
        Database_query.simple_type_without_return(name_query, query_to_db)

    @staticmethod
    def update_tournament_details_for_notification(link):
        query_to_db = f"UPDATE tournament_go SET details = 'for_mailing' WHERE link = '{link}';"
        name_query = "update_tournament_details"
        Database_query.simple_type_without_return(name_query, query_to_db)

    def get_adult_tournaments_in_city(self):
        name_query = "get_adult_tournaments_in_city"
        array = []
        query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      "WHERE is_child = 0;"
        array = SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)
        if len(array) > 0:
            return array
        else:
            return None

    def tournaments_for_user(self):
        name_query = "tournaments_for_user"
        array = []
        query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      "WHERE is_new = 'yes';"
        return SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)

    def details_of_tournament_exist_for_user(self):
        name_query = "details_of_tournament_exist_for_user"
        array = []
        query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      "WHERE details = 'for_mailing';"
        return SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)

    def tournaments_for_user_adult(self):
        name_query = "tournaments_for_user_adult"
        array = []
        query_to_db = f"SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      f"WHERE is_child = 0 " \
                      f"AND is_new = 'yes';"
        return SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)

    def details_of_tournament_exist_for_user_adult(self):
        name_query = "details_of_tournament_exist_for_user"
        array = []
        query_to_db = "SELECT t_start, t_end, t_name, CityID, link, is_child FROM tournament_go " \
                      "WHERE details = 'for_mailing' AND is_child = 0;"
        return SendTournament.send_tournament(self.chat_id, name_query, array, query_to_db)

    @staticmethod
    def check_details():
        try:
            tournaments_without_details = Tournament_go.all_tournaments_without_details()
            file = 'APP/html/check_details.html'
            string = 'предварительная регистрация'
            for tournament in tournaments_without_details:
                Parsing.download_page(tournament[0], file)
                Parsing.record_set(file)
                if Parsing.check_string(string, file):
                    Tournament_go.update_tournament_details_for_notification(tournament[0])
                os.system(r'cat /dev/null>APP/html/check_details.html')
            #log(0, "checking the details is over", logging.INFO)
        except FileNotFoundError as e:
            log(0, f"error {e}", logging.ERROR)
