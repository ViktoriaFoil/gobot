import requests
import os
from bs4 import BeautifulSoup
import datetime
import logging
import tournament
import log
import mysql_dbconfig
import BOT.bot as app


def date():
    today = datetime.now().date()
    return today


# download the current version
def download_page(url, name):
    try:
        r = requests.get(url)
        log.log(0, "download page " + url, logging.INFO)
        with open(name, 'w') as output_file:
            output_file.write(r.text.replace("&nbsp;-&nbsp;", ""))
            log.log(0, "save url to " + name, logging.INFO)
        r.close()
    except Exception as e:
        log.log(0, "error download page: " + str(e), logging.ERROR)


# remove line breaks
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
        log.log(0, "error record set: " + str(e), logging.ERROR)


# write down the differences
def compare(current_page, old_page):
    try:
        old_records = record_set(old_page)
        log.log(0, "record set: " + old_page, logging.INFO)
        current_records = record_set(current_page)
        log.log(0, "record set " + current_page, logging.INFO)
        open('BOT/difference.html', 'w').close()
        new_records = []

        with open('BOT/difference.html', 'a') as f:
            for line in current_records:
                if line not in old_records:
                    new_records.append(line)
            f.writelines(new_records)
            log.log(0, "save to difference.html", logging.INFO)
    except Exception as e:
        log.log(0, "error compare: " + str(e), logging.ERROR)


# write to old page
def copy_current_to_old(old_page, current_page):
    try:
        with open(current_page, 'r') as current:
            with open(old_page, 'w') as old:
                old.write(current.read())
                old.close()
                current.close()
                log.log(0, "information overwritten", logging.INFO)
    except Exception as e:
        log.log(0, "error copy current to old: " + str(e), logging.ERROR)


def check_exist_file(name):
    if not os.path.isfile(name):
        with open(name, 'w'): pass


# add tournaments to db
def insert_tournament(tournaments):
    for tour in tournaments:
        query = "INSERT INTO tournament_go (t_start, t_end, t_name, CityID, link, is_child) " \
                "VALUES(%s, %s, %s, %s, %s, %s)"

        try:
            city_id = int(app.Cities.get_CityId_By_Name(tour.city))
            mysql_dbconfig.cursor.execute(query, [tour.start, tour.end, tour.name, city_id, tour.link, tour.flag])
            mysql_dbconfig.conn.commit()
        except BaseException as e:
            log.log(0, "error insert tournament: " + str(e), logging.ERROR)


# link two functions insert_tournament and getText
def main():
    try:
        tournaments = get_text()
        insert_tournament(tournaments)
        log.log(0, "successful entry of new tournaments into the database", logging.INFO)
    except BaseException as e:
        log.log(0, "error main: " + str(e), logging.ERROR)


# get text for tournaments
def get_text():
    html = open('BOT/difference.html')
    root = BeautifulSoup(html, 'lxml')
    tr = root.select('tr')
    tournaments = []

    for t in tr:
        a = t.select('a')
        tour = tournament.Tournament()
        len_array = len(t.contents)

        if "padding-right" in str(t):
            if len_array == 5:
                start_date = t.contents[1].text
                tour.setStart(str(start_date))

                end_date = t.contents[2].text
                tour.setEnd(str(end_date))

                t_name = t.contents[3].text
                is_child = 0
                for categories in app.Children_categories().set_children_categories():
                    if categories[0] in t_name:
                        is_child = 1
                        tour.setFlag(is_child)
                tour.setFlag(is_child)
                tour.setName(t_name)

                link = "https://gofederation.ru" + str(a[0].attrs['href'])
                tour.setLink(link)

                city = t.contents[4].text \
                    .replace("Сервер", "") \
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

                tour.setCity(city)
                tournaments.append(tour)

            if len_array == 4:
                start_date = t.contents[0].text
                tour.setStart(str(start_date))

                end_date = t.contents[1].text
                tour.setEnd(str(end_date))

                t_name = t.contents[2].text
                is_child = 0
                for categories in app.Children_categories().set_children_categories():
                    if categories[0] in t_name:
                        is_child = 1
                        tour.setFlag(is_child)
                tour.setFlag(is_child)
                tour.setName(t_name)

                link = "https://gofederation.ru" + str(a[0].attrs['href'])
                tour.setLink(link)

                city = t.contents[3].text \
                    .replace("Сервер", "") \
                    .replace(", КГС", "") \
                    .replace(", KGS", "") \
                    .replace(", OGS", "") \
                    .replace(" (КГС)", "") \
                    .replace(" (ОГС)", "") \
                    .replace(", ОГС", "") \
                    .replace("OGS", "ОГС") \
                    .replace("KGS", "КГС") \
                    .replace(", GoQuest", "") \
                    .replace(" (GoQuest)", "") \
                    .replace("г. ", "") \
                    .replace("сервер, ", "") \
                    .replace(" Pandanet", "") \
                    .replace(", Pandanet", "")

                tour.setCity(city)
                tournaments.append(tour)

            continue

    return tournaments
