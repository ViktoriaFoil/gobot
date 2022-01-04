import datetime
import locale
import logging

from APP.config.mysql import Mysql
from APP.logs.log import log
from APP.queries_to_tables.cities import Cities
from APP.queries_to_tables.usercity import User_City


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
            Mysql.cursor.execute(query)
            result = Mysql.cursor.fetchall()
            city_user = User_City(chat_id).get_cities_for_user()

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
                        break

            return array

        except BaseException as e:
            log(0, f"error {name_query} {e}", logging.ERROR)
