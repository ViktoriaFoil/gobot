import datetime
import re

import requests
import logging
from bs4 import BeautifulSoup

from config.mysql import cursor, conn
from queries_to_tables.cities import Cities
from logs.log import log
from objects.tournament import Tournament
from queries_to_tables.children_categories import Children_categories


class Parsing:

    @staticmethod
    def date():
        today = datetime.now().date()
        return today

    # download the current version
    @staticmethod
    def download_page(url, name):
        try:
            r = requests.get(url)
            log(0, "download page " + url, logging.INFO)
            with open(name, 'w') as output_file:
                output_file.write(r.text.replace("&nbsp;-&nbsp;", ""))
                log(0, "save url to " + name, logging.INFO)
            r.close()
        except Exception as e:
            log(0, "error download page: " + str(e), logging.ERROR)

    # remove line breaks
    @staticmethod
    def record_set(page):
        try:
            with open(page, 'r') as f:
                content = f.read().replace('\n', '')
                soup = BeautifulSoup(content, 'lxml')
                result_set = set()
                for item in soup.find_all("tr"):
                    result_set.add(str(item))
                return result_set
        except Exception as e:
            log(0, "error record set: " + str(e), logging.ERROR)

    # write down the differences
    @staticmethod
    def compare(current_page, old_page):
        try:
            old_records = Parsing.record_set(old_page)
            log(0, "record set: " + old_page, logging.INFO)
            current_records = Parsing.record_set(current_page)
            log(0, "record set " + current_page, logging.INFO)
            open('APP/html/difference.html', 'w').close()
            new_records = []

            with open('APP/html/difference.html', 'a') as f:
                for line in current_records:
                    if line not in old_records:
                        new_records.append(line)
                f.writelines(new_records)
                log(0, "save to difference.html", logging.INFO)
        except Exception as e:
            log(0, "error compare: " + str(e), logging.ERROR)

    # write to old page
    @staticmethod
    def copy_current_to_old(old_page, current_page):
        try:
            with open(current_page, 'r') as current:
                with open(old_page, 'w') as old:
                    old.write(current.read())
                    old.close()
                    current.close()
                    log(0, "information overwritten", logging.INFO)
        except Exception as e:
            log(0, "error copy current to old: " + str(e), logging.ERROR)

    # @staticmethod
    # def check_exist_file(name):
    #    if not os.path.isfile(name):
    #        with open(name, 'w'): pass

    # link two functions insert_tournament and getText
    @staticmethod
    def main(not_exist_tournament):
        try:
            if not_exist_tournament:
                tournaments = Parsing.get_text_first()
            else:
                tournaments = Parsing.get_text()
            Parsing.insert_tournament(tournaments)
            log(0, "successful entry of new tournaments into the database", logging.INFO)
        except BaseException as e:
            log(0, "error main: " + str(e), logging.ERROR)

    @staticmethod
    def insert_tournament(tournaments):
        for tour in tournaments:
            query = "INSERT INTO tournament_go (t_start, t_end, t_name, CityID, link, is_child) " \
                    "VALUES(%s, %s, %s, %s, %s, %s);"

            try:
                city_id = int(Cities.get_CityId_By_Name(tour.city))
                cursor.execute(query, [tour.start, tour.end, tour.name, city_id, tour.link, tour.flag])
                conn.commit()
            except BaseException as e:
                log(0, f"error insert tournament: {e}", logging.ERROR)

    @staticmethod
    def make_correct_format(namecity):
        correct_format = namecity.replace("Сервер", "") \
            .replace(", КГС", "") \
            .replace(", KGS", "") \
            .replace(", OGS", "") \
            .replace("(КГС)", "") \
            .replace("(ОГС)", "") \
            .replace(", ОГС", "") \
            .replace("OGS", "ОГС") \
            .replace("KGS", "КГС") \
            .replace(", GoQuest", "") \
            .replace(" (GoQuest)", "") \
            .replace("г. ", "") \
            .replace("сервер, ", "")
        return correct_format

    # get text for tournaments
    @staticmethod
    def get_text():
        html = open('APP/html/difference.html')
        root = BeautifulSoup(html, 'lxml')
        tr = root.select('tr')
        tournaments = []

        for t in tr:
            a = t.select('a')
            tour = Tournament()
            len_array = len(t.contents)

            if "padding-right" in str(t):
                if len_array == 5:
                    start_date = t.contents[1].text
                    tour.setStart(str(start_date))

                    end_date = t.contents[2].text
                    tour.setEnd(str(end_date))

                    t_name = t.contents[3].text
                    is_child = 0
                    for categories in Children_categories.set_children_categories():
                        if categories[0] in t_name:
                            is_child = 1
                            tour.setFlag(is_child)
                    tour.setFlag(is_child)
                    tour.setName(t_name)

                    link = "https://gofederation.ru" + str(a[0].attrs['href'])
                    tour.setLink(link)

                    getcity = t.contents[4].text
                    city = Parsing.make_correct_format(getcity)

                    tour.setCity(city)
                    tournaments.append(tour)

                if len_array == 4:
                    start_date = t.contents[0].text
                    tour.setStart(str(start_date))

                    end_date = t.contents[1].text
                    tour.setEnd(str(end_date))

                    t_name = t.contents[2].text
                    is_child = 0
                    for categories in Children_categories.set_children_categories():
                        if categories[0] in t_name:
                            is_child = 1
                            tour.setFlag(is_child)
                    tour.setFlag(is_child)
                    tour.setName(t_name)

                    link = "https://gofederation.ru" + str(a[0].attrs['href'])
                    tour.setLink(link)

                    getcity = t.contents[3].text
                    city = Parsing.make_correct_format(getcity)

                    tour.setCity(city)
                    tournaments.append(tour)

                continue

        return tournaments

    @staticmethod
    def get_text_first():
        html = open('APP/html/current.html')
        root = BeautifulSoup(html, 'lxml')
        tr = root.select('tr')
        tournaments = []

        for t in tr:
            a = t.select('a')
            tour = Tournament()
            len_array = len(t.contents)

            if "padding-right" in str(t):
                if len_array == 5:
                    start_date = t.contents[1].text
                    tour.setStart(str(start_date))

                    end_date = t.contents[2].text
                    tour.setEnd(str(end_date))

                    t_name = t.contents[3].text
                    is_child = 0
                    for categories in Children_categories.set_children_categories():
                        if categories[0] in t_name:
                            is_child = 1
                            tour.setFlag(is_child)
                    tour.setFlag(is_child)
                    tour.setName(t_name)

                    link = "https://gofederation.ru" + str(a[0].attrs['href'])
                    tour.setLink(link)

                    getcity = t.contents[4].text
                    city = Parsing.make_correct_format(getcity)

                    tour.setCity(city)
                    tournaments.append(tour)

                if len_array == 4:
                    start_date = t.contents[0].text
                    tour.setStart(str(start_date))

                    end_date = t.contents[1].text
                    tour.setEnd(str(end_date))

                    t_name = t.contents[2].text
                    is_child = 0
                    for categories in Children_categories.set_children_categories():
                        if categories[0] in t_name:
                            is_child = 1
                            tour.setFlag(is_child)
                    tour.setFlag(is_child)
                    tour.setName(t_name)

                    link = "https://gofederation.ru" + str(a[0].attrs['href'])
                    tour.setLink(link)

                    getcity = t.contents[3].text
                    city = Parsing.make_correct_format(getcity)

                    tour.setCity(city)
                    tournaments.append(tour)

                continue

        return tournaments

    @staticmethod
    def check_string(string, file):
        with open(file) as f:
            found = False
            for line in f:
                if re.search(string, line):
                    found = True
            return found
