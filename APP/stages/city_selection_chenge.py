import os
import telebot
from telebot import types
import logging

from APP.logs.log import log
from APP.queries_to_tables.cities import Cities
from APP.queries_to_tables.keyboards import Keyboards
from APP.queries_to_tables.user_botgo import User_botgo
from APP.queries_to_tables.usercity import User_City

token = os.getenv("BOT")
bot = telebot.TeleBot(token)
state = "city_selection"
listCity = []


class City_selection_chenge:

    @staticmethod
    def message_state_city_selection(message):

        towns = types.ReplyKeyboardMarkup(resize_keyboard=True)
        age = Keyboards.get_keyboard("age")
        navigation = Keyboards.get_keyboard("navigation")

        all_city = sorted(set(Cities.get_all_cities()) - set(listCity))
        for city in all_city:
            towns.add(types.KeyboardButton(city))

        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Привет, выбери города 🏘, в которых турниры актуальны для тебя 😉',
                             reply_markup=towns)
            log(message.chat.id, "send command /start", logging.INFO)

        if message.html_text in all_city:
            User_City(message.chat.id).add_city(message.html_text)
            listCity.append(message.html_text)
            bot.send_message(message.chat.id, 'Если хочешь выбрать еще города, нажми ДАЛЕЕ, если нет, то нажми СТОП',
                             reply_markup=navigation)
            log(message.chat.id, "user selects a city", logging.INFO)

        if message.html_text == 'далее':
            bot.send_message(message.chat.id, 'Выбери город', reply_markup=towns)
            log(message.chat.id, "the user selects an additional city", logging.INFO)

        if message.html_text == 'стоп':
            User_botgo(message.chat.id).query_change_state("age_category")
            bot.send_message(message.chat.id, 'Выбери свою категорию. Это нужно, чтобы я фильтровал для тебя турниры. '
                                              'В категории я ребенок, присылаюся все турниры. '
                                              'В категории я взрослый, только взрослые турниры.', reply_markup=age)
            log(message.chat.id, "the user has selected all the cities that interest him,  \
                                      switched to the age selection state", logging.INFO)
            listCity.clear()

    # =======================================================================================================

    @staticmethod
    def message_state_city_change(message):

        towns = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mainButton = Keyboards.get_keyboard("main")
        navigation = Keyboards.get_keyboard("navigation")

        all_city = sorted(set(Cities(message.chat.id).get_all_cities()) - set(listCity))
        for city in all_city:
            towns.add(types.KeyboardButton(city))

        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Выбери города 😉', reply_markup=towns)
            log(message.chat.id, "user changes cities", logging.INFO)

        if message.html_text in all_city:
            User_City(message.chat.id).add_city(message.html_text)
            listCity.append(message.html_text)
            bot.send_message(message.chat.id, 'Если хочешь выбрать еще города, \
                                                нажми ДАЛЕЕ, если нет, то нажми СТОП',
                             reply_markup=navigation)

        if message.html_text == 'далее':
            bot.send_message(message.chat.id, 'Выбери город', reply_markup=towns)

        if message.html_text == 'стоп':
            User_botgo(message.chat.id).query_change_state('main')
            bot.send_message(message.chat.id, 'Смена городов произведена успешно', reply_markup=mainButton)
            log(message.chat.id, "the user has successfully changed cities", logging.INFO)
            listCity.clear()
