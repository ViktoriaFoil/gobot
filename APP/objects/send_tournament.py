import datetime
import locale
import logging

from config.mysql import cursor
from logs.log import log
from queries_to_tables.cities import Cities
from queries_to_tables.usercity import User_City
LC_TIME="ru_RU.UTF-8"


class SendTournament:
    start: str
    end: str
    name: str
    city: str
    link: str

    def __init__(self,
                 start: str,
                 end: str,
                 name: str,
                 city: str,
                 link: str):
        self.start = start
        self.end = end
        self.name = name
        self.city = Cities.get_CityName_By_Id(city)
        self.link = link

    @staticmethod
    def send_tournament(chat_id, name_query, array, query):
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            city_user = User_City(chat_id).get_user_subscription_city()

            for city in city_user:
                for res in result:
                    tournament = SendTournament(start=res[0],
                                                end=res[1],
                                                name=res[2],
                                                city=res[3],
                                                link=res[4])
                    cityinres = res[3]
                    if str(cityinres) == str(city):
                        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
                        format_string = "%Y-%m-%d"
                        start = datetime.datetime.strptime(f"{tournament.start}", format_string).strftime("%d %B %Y")
                        end = datetime.datetime.strptime(f"{tournament.end}", format_string).strftime("%d %B %Y")
                        tournament = f"Начало: {start}\n" \
                                     f"Конец: {end}\n\n" \
                                     f"Название: {tournament.name}\n\n" \
                                     f"Город: {tournament.city}\n\n" \
                                     f"Подробнее: {tournament.link}\n"
                        array.append(tournament)

            return array

        except Exception as e:
            log(0, f"error {name_query} {e}", logging.ERROR)
