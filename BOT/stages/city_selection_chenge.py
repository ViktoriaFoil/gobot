import os
import telebot
from telebot import types
import logging
from BOT import log
import BOT.bot as app

token = os.getenv("BOT")
bot = telebot.TeleBot(token)
state = "city_selection"
listCity = []

class City_selection_chenge:

    def message_state_city_selection(self, message):

        towns = types.ReplyKeyboardMarkup(resize_keyboard=True)
        age = app.Keyboards().get_keyboard("age")
        navigation = app.Keyboards().get_keyboard("navigation")

        all_city = sorted(set(app.Cities().get_all_cities()) - set(listCity))
        for city in all_city:
            towns.add(types.KeyboardButton(city))

        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Привет, выбери города 🏘, в которых турниры актуальны для тебя 😉', reply_markup=towns)
            log.log(message.chat.id, "send command /start", logging.INFO)


        if message.html_text in all_city:
            app.Usercity().add_city(message.chat.id, message.html_text)
            listCity.append(message.html_text)
            bot.send_message(message.chat.id, 'Если хочешь выбрать еще города, нажми ДАЛЕЕ, если нет, то нажми СТОП', reply_markup=navigation)
            log.log(message.chat.id, "user selects a city", logging.INFO)


        if message.html_text == 'далее':
            bot.send_message(message.chat.id, 'Выбери город', reply_markup=towns)
            log.log(message.chat.id, "the user selects an additional city", logging.INFO)


        if message.html_text == 'стоп':
            app.User_botgo().query_change_state("age_category", message.chat.id)
            bot.send_message(message.chat.id, 'Выбери свою категорию. Это нужно, чтобы я фильтровал для тебя турниры. В категории я ребенок, присылаюся все турниры. В категории я взрослый, только взрослые турниры.', reply_markup=age)
            log.log(message.chat.id, "the user has selected all the cities that interest him, switched to the age selection state", logging.INFO)
            listCity.clear()

#=======================================================================================================


    def message_state_city_change(self, message):

        towns = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mainButton = app.Keyboards().get_keyboard("main")
        navigation = app.Keyboards().get_keyboard("navigation")

        all_city = sorted(set(app.Cities().get_all_cities()) - set(listCity))
        for city in all_city:
            towns.add(types.KeyboardButton(city))

        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Выбери города 😉', reply_markup=towns)
            log.log(message.chat.id, "user changes cities", logging.INFO)

        if message.html_text in all_city:
            app.Usercity().add_city(message.chat.id, message.html_text)
            listCity.append(message.html_text)
            bot.send_message(message.chat.id, 'Если хочешь выбрать еще города, нажми ДАЛЕЕ, если нет, то нажми СТОП', reply_markup=navigation)

        if message.html_text == 'далее':
            bot.send_message(message.chat.id, 'Выбери город', reply_markup=towns)

        if message.html_text == 'стоп':
            app.User_botgo().query_change_state('main', message.chat.id)
            bot.send_message(message.chat.id, 'Смена городов произведена успешно', reply_markup=mainButton)
            log.log(message.chat.id, "the user has successfully changed cities", logging.INFO)
            listCity.clear()
